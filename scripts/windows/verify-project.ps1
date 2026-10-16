param([switch]$Json)
$ErrorActionPreference = 'Stop'
$sw = [Diagnostics.Stopwatch]::StartNew()
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

Write-Host '=== VALIANT2 BIRLESIK PROJE & KAYNAK BUTUNLUK DENETLEYICISI ===' -ForegroundColor Cyan

# 1. Controls.h Flag Synchronization Audit
$clientControls = Join-Path $root 'source\client\source\Controls.h'
$serverControls = Join-Path $root 'source\server\source\common\Controls.h'

function Get-DefinesFromFile([string]$path) {
    $defines = @{}
    if (!(Test-Path $path)) { return $defines }
    foreach ($line in [IO.File]::ReadAllLines($path)) {
        $t = $line.Trim()
        if ($t -match '^#define\s+([A-Za-z0-9_]+)') {
            $defines[$Matches[1]] = $true
        } elseif ($t -match '^//\s*#define\s+([A-Za-z0-9_]+)') {
            if (!$defines.ContainsKey($Matches[1])) {
                $defines[$Matches[1]] = $false
            }
        }
    }
    return $defines
}

$cDefs = Get-DefinesFromFile $clientControls
$sDefs = Get-DefinesFromFile $serverControls
$sharedKeys = $cDefs.Keys | Where-Object { $sDefs.ContainsKey($_) } | Sort-Object
$mismatchedFlags = @()
foreach ($k in $sharedKeys) {
    if ($cDefs[$k] -ne $sDefs[$k]) {
        $mismatchedFlags += [PSCustomObject]@{
            Flag = $k
            Client = if ($cDefs[$k]) { 'ON' } else { 'OFF' }
            Server = if ($sDefs[$k]) { 'ON' } else { 'OFF' }
        }
    }
}

Write-Host ("[1/6] Controls.h Bayrak Denetimi: Client={0} / Server={1} / Ortak={2} / Uyumsuz={3}" -f $cDefs.Count, $sDefs.Count, $sharedKeys.Count, $mismatchedFlags.Count) -ForegroundColor Green
foreach ($m in $mismatchedFlags) {
    Write-Host ("  ! Bayrak farki: {0} (Client={1}, Server={2})" -f $m.Flag, $m.Client, $m.Server) -ForegroundColor Yellow
}

# 2. Packet Header Collision Audit
$serverPacketFile = Join-Path $root 'source\server\source\game\src\packet.h'
$cgHeaders = @{}
$gcHeaders = @{}
$packetCollisions = @()
if (Test-Path $serverPacketFile) {
    foreach ($line in [IO.File]::ReadAllLines($serverPacketFile)) {
        $t = $line.Trim()
        if ($t -match '^(HEADER_CG_[A-Za-z0-9_]+)\s*=\s*(\d+)') {
            $name = $Matches[1]; $val = [int]$Matches[2]
            if ($cgHeaders.ContainsKey($val)) {
                $packetCollisions += "CG Header Cakismasi ($val): $($cgHeaders[$val]) <-> $name"
            } else { $cgHeaders[$val] = $name }
        } elseif ($t -match '^(HEADER_GC_[A-Za-z0-9_]+)\s*=\s*(\d+)') {
            $name = $Matches[1]; $val = [int]$Matches[2]
            if ($gcHeaders.ContainsKey($val)) {
                $packetCollisions += "GC Header Cakismasi ($val): $($gcHeaders[$val]) <-> $name"
            } else { $gcHeaders[$val] = $name }
        }
    }
}
Write-Host ("[2/6] Paket Basligi (Packet.h) Denetimi: CG={0} / GC={1} / Cakisma={2}" -f $cgHeaders.Count, $gcHeaders.Count, $packetCollisions.Count) -ForegroundColor Green

# 3. AtlasInfo Sector & 25600 Alignment / Overlap Check
$atlasFile = Join-Path $root 'assets\unpacked\data\config\general\atlasinfo.txt'
$atlasSectors = @()
$atlasWarnings = @()
if (Test-Path $atlasFile) {
    foreach ($line in [IO.File]::ReadAllLines($atlasFile)) {
        $t = $line.Trim()
        if (!$t -or $t.StartsWith('#') -or $t.StartsWith('//')) { continue }
        $parts = $t -split '\s+'
        if ($parts.Count -ge 5) {
            $mapName = $parts[0]
            $bx = [long]$parts[1]; $by = [long]$parts[2]
            $wx = [int]$parts[3];  $wy = [int]$parts[4]
            if (($bx % 25600) -ne 0 -or ($by % 25600) -ne 0) {
                $atlasWarnings += "25600 hiza uyarisi: $mapName ($bx, $by)"
            }
            $atlasSectors += [PSCustomObject]@{
                Name = $mapName; X1 = $bx; Y1 = $by
                X2 = $bx + ($wx * 25600); Y2 = $by + ($wy * 25600)
                W = $wx; H = $wy
            }
        }
    }
}
Write-Host ("[3/6] AtlasInfo Harita Sektor Denetimi: Toplam Harita={0} / Hiza Uyarisi={1}" -f $atlasSectors.Count, $atlasWarnings.Count) -ForegroundColor Green

# 4. Quest List & Collection Verification
$questDir = Join-Path $root 'runtime\server\main\srv1\share\locale\europe\quest'
$questListFile = Join-Path $questDir 'quest_list'
$missingQuests = @()
$totalQuests = 0
if (Test-Path $questListFile) {
    foreach ($line in [IO.File]::ReadAllLines($questListFile)) {
        $q = $line.Trim()
        if (!$q -or $q.StartsWith('#')) { continue }
        $totalQuests++
        $qPath = Join-Path $questDir ($q -replace '/', '\')
        if (!(Test-Path $qPath)) { $missingQuests += $q }
    }
}
Write-Host ("[4/6] Quest Koleksiyonu Denetimi: Kayitli={0} / Eksik Dosya={1}" -f $totalQuests, $missingQuests.Count) -ForegroundColor Green
foreach ($mq in $missingQuests) {
    Write-Host ("  ! Eksik Quest: {0}" -f $mq) -ForegroundColor Red
}

# 5. Unsafe DirectQuery(variable) Format-String Crash Audit
$gameSrcDir = Join-Path $root 'source\server\source\game\src'
$unsafeQueries = @()
if (Test-Path $gameSrcDir) {
    foreach ($cppFile in Get-ChildItem $gameSrcDir -Filter '*.cpp' -File) {
        $lineNum = 0
        foreach ($line in [IO.File]::ReadAllLines($cppFile.FullName)) {
            $lineNum++
            $t = $line.Trim()
            if ($t.StartsWith('//')) { continue }
            if ($t -match 'DirectQuery\s*\(\s*([A-Za-z_][A-Za-z0-9_\.\->\(\)]*)\s*\)') {
                $argExpr = $Matches[1]
                $unsafeQueries += "$($cppFile.Name):$lineNum -> DirectQuery($argExpr) [DirectQuery(""%s"", ...) kullanin!]"
            }
        }
    }
}
Write-Host ("[5/6] C++ DirectQuery Format-String Denetimi: Riskli Cagri={0}" -f $unsafeQueries.Count) -ForegroundColor $(if ($unsafeQueries.Count -eq 0) { 'Green' } else { 'Yellow' })
foreach ($uq in $unsafeQueries) {
    Write-Host ("  ! $uq") -ForegroundColor Yellow
}

# 6. Server & Client Syserr / Crash Dump Health Audit
$srvDir = Join-Path $root 'runtime\server\main\srv1'
$crashDumps = @(Get-ChildItem $srvDir -Recurse -Filter '*.dmp' -ErrorAction SilentlyContinue)
$clientSyserrDir = Join-Path $root 'runtime\client\game\syserr'
$latestClientSyserr = Get-ChildItem $clientSyserrDir -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$clientSyserrCount = 0
if ($latestClientSyserr -and $latestClientSyserr.Length -gt 0) {
    $clientSyserrCount = @(Get-Content $latestClientSyserr.FullName | Where-Object { $_.Trim() -ne '' }).Count
}
Write-Host ("[6/6] Runtime Crash (.dmp) & Syserr Denetimi: Sunucu Dump={0} / Son Istemci Syserr Satiri={1}" -f $crashDumps.Count, $clientSyserrCount) -ForegroundColor $(if ($crashDumps.Count -eq 0) { 'Green' } else { 'Red' })

$sw.Stop()
Write-Host ("Denetim {0} sn icinde tamamlandi." -f [math]::Round($sw.Elapsed.TotalSeconds, 2)) -ForegroundColor Cyan
