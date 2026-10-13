param([switch]$Minimal)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
& (Join-Path $PSScriptRoot 'sync-config.ps1')
$serviceName = 'MariaDB'
$line = Get-Content (Join-Path $root '.env') | Where-Object { $_ -match '^MARIADB_SERVICE=' } | Select-Object -First 1
if ($line) { $serviceName = $line.Split('=', 2)[1].Trim() }
$service = Get-Service -Name $serviceName -ErrorAction Stop
if ($service.Status -ne 'Running') {
    Start-Service $serviceName
    $service.WaitForStatus('Running', [TimeSpan]::FromSeconds(30))
}
$serverRoot = Join-Path $root 'runtime\server\main\srv1'
$bin = Join-Path $serverRoot 'share\bin'
$processes = @(
    @{ Name = 'valiant-db'; File = (Join-Path $bin 'db.exe'); WorkingDirectory = (Join-Path $serverRoot 'db') },
    @{ Name = 'valiant-auth'; File = (Join-Path $bin 'game.exe'); WorkingDirectory = (Join-Path $serverRoot 'auth') }
)
$coreDirectories = if ($Minimal) {
    Get-Item (Join-Path $serverRoot 'chan\ch1\core1')
} else {
    Get-ChildItem (Join-Path $serverRoot 'chan') -Directory -Recurse | Where-Object { $_.Name -like 'core*' }
}
$coreDirectories | Sort-Object FullName | ForEach-Object {
    $processes += @{ Name = "valiant-$($_.Parent.Name)-$($_.Name)"; File = (Join-Path $bin 'game.exe'); WorkingDirectory = $_.FullName }
}
$stateDir = Join-Path $root 'runtime\server\.state'
New-Item -ItemType Directory -Force -Path $stateDir | Out-Null
foreach ($entry in $processes) {
    $process = Start-Process -FilePath $entry.File -WorkingDirectory $entry.WorkingDirectory -WindowStyle Hidden -PassThru
    Set-Content -Path (Join-Path $stateDir "$($entry.Name).pid") -Value $process.Id -Encoding ascii
    Write-Host "$($entry.Name) started (PID $($process.Id))."
    # db.exe icin port hazir olana kadar bekle (diger surec icin 3sn)
    if ($entry.Name -eq 'valiant-db') {
        $dbPort = 30000
        for ($i = 0; $i -lt 30; $i++) {
            if ($process.HasExited) { throw "$($entry.Name) exited with code $($process.ExitCode)." }
            try { $tcp = New-Object Net.Sockets.TcpClient; $tcp.Connect('127.0.0.1', $dbPort); $tcp.Close(); Write-Host "  db port $dbPort ready."; break } catch { Start-Sleep -Seconds 1 }
        }
    } else {
        # Wait a few seconds and check the process is still alive
        Start-Sleep -Seconds 5
        if ($process.HasExited) { throw "$($entry.Name) exited with code $($process.ExitCode)." }
    }
}
