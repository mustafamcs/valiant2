param([switch]$Minimal)
$ErrorActionPreference = 'Stop'
$sw = [Diagnostics.Stopwatch]::StartNew()
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
. (Join-Path $PSScriptRoot 'common.ps1')
$hw = Optimize-HardwareConfig

& (Join-Path $PSScriptRoot 'sync-config.ps1')

$serviceName = 'MariaDB'
$line = Get-Content (Join-Path $root '.env') -ErrorAction SilentlyContinue | Where-Object { $_ -match '^MARIADB_SERVICE=' } | Select-Object -First 1
if ($line) { $serviceName = $line.Split('=', 2)[1].Trim() }
$service = Get-Service -Name $serviceName -ErrorAction Stop
if ($service.Status -ne 'Running') {
    Start-Service $serviceName
    $service.WaitForStatus('Running', [TimeSpan]::FromSeconds(15))
}

$serverRoot = Join-Path $root 'runtime\server\main\srv1'
$bin = Join-Path $serverRoot 'share\bin'
$stateDir = Join-Path $root 'runtime\server\.state'
New-Item -ItemType Directory -Force -Path $stateDir | Out-Null

# Eskiden kalma sunucu sureclerini temizle
Get-Process -Name 'game','db' -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# 1) Once db.exe'yi baslat ve 30000 portunu 40ms araliklarla bekle (tipik ~300ms)
$dbEntry = @{ Name = 'valiant-db'; File = (Join-Path $bin 'db.exe'); WorkingDirectory = (Join-Path $serverRoot 'db'); Port = 30000 }
$dbProc = Start-Process -FilePath $dbEntry.File -WorkingDirectory $dbEntry.WorkingDirectory -WindowStyle Hidden -PassThru
try { $dbProc.PriorityClass = 'High' } catch {}
Set-Content -Path (Join-Path $stateDir 'valiant-db.pid') -Value $dbProc.Id -Encoding ascii

$dbReady = $false
for ($i = 0; $i -lt 250; $i++) {
    if ($dbProc.HasExited) { throw "valiant-db exited with code $($dbProc.ExitCode)." }
    $listening = @([Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners() | ForEach-Object { $_.Port })
    if ($listening -contains 30000) {
        $dbReady = $true
        break
    }
    Start-Sleep -Milliseconds 40
}
if (-not $dbReady) { throw 'valiant-db port 30000 zaman asimina ugradi.' }
$elDb = [math]::Round($sw.Elapsed.TotalSeconds, 2)
Write-Host "valiant-db started (PID $($dbProc.Id)) - port 30000 hazir ($elDb sn)."

# 2) Auth ve tum oyun core'larini AYNI ANDA PARALEL baslat!
$coreEntries = @(
    @{ Name = 'valiant-auth'; File = (Join-Path $bin 'game.exe'); WorkingDirectory = (Join-Path $serverRoot 'auth'); Port = 30001 }
)
if ($Minimal) {
    $coreEntries += @{ Name = 'valiant-ch1-core1'; File = (Join-Path $bin 'game.exe'); WorkingDirectory = (Join-Path $serverRoot 'chan\ch1\core1'); Port = 30003 }
} else {
    $portMap = @{ 'core1' = 30003; 'core2' = 30005; 'core3' = 30007; 'core4' = 30009; 'core99' = 30051 }
    Get-ChildItem (Join-Path $serverRoot 'chan') -Directory -Recurse | Where-Object { $_.Name -like 'core*' } | Sort-Object FullName | ForEach-Object {
        $p = if ($portMap.ContainsKey($_.Name)) { $portMap[$_.Name] } else { 0 }
        $coreEntries += @{ Name = "valiant-$($_.Parent.Name)-$($_.Name)"; File = (Join-Path $bin 'game.exe'); WorkingDirectory = $_.FullName; Port = $p }
    }
}

$startedCores = @()
foreach ($entry in $coreEntries) {
    $proc = Start-Process -FilePath $entry.File -WorkingDirectory $entry.WorkingDirectory -WindowStyle Hidden -PassThru
    try { $proc.PriorityClass = 'AboveNormal' } catch {}
    Set-Content -Path (Join-Path $stateDir "$($entry.Name).pid") -Value $proc.Id -Encoding ascii
    $startedCores += [pscustomobject]@{ Name = $entry.Name; Process = $proc; Port = $entry.Port; Ready = ($entry.Port -eq 0) }
}

# Tum core portlarinin acilmasini soket baglantisi acmadan (syserr olusturmadan) OS tablosundan 40ms araliklarla bekle
for ($i = 0; $i -lt 250; $i++) {
    $listening = @([Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners() | ForEach-Object { $_.Port })
    $allReady = $true
    foreach ($c in $startedCores) {
        if ($c.Process.HasExited) { throw "$($c.Name) exited with code $($c.Process.ExitCode)." }
        if (-not $c.Ready) {
            if ($listening -contains $c.Port) {
                $c.Ready = $true
                Write-Host "$($c.Name) ready (PID $($c.Process.Id), port $($c.Port))."
            } else {
                $allReady = $false
            }
        }
    }
    if ($allReady) { break }
    Start-Sleep -Milliseconds 40
}

$sw.Stop()
$elTotal = [math]::Round($sw.Elapsed.TotalSeconds, 2)
Write-Host "Tum oyun sunucusu corelari $elTotal saniyede hiper-hizli baslatildi! [$($hw.CpuName)]"
