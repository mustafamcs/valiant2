param([switch]$NoReload, [switch]$NoRestart)
$ErrorActionPreference = 'Stop'
$sw = [Diagnostics.Stopwatch]::StartNew()
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
. (Join-Path $PSScriptRoot 'common.ps1')

$serverWasRunning = [bool](Get-Process -Name 'game','db' -ErrorAction SilentlyContinue)
Write-Host 'Quest derlemesi oncesi game.exe + db.exe + qc.exe kapatiliyor...'
Stop-ServerProcesses

$questDir = Join-Path $root 'runtime\server\main\srv1\share\locale\europe\quest'
$qcExe = Join-Path $questDir 'qc.exe'

if (!(Test-Path $qcExe)) {
    Write-Host 'qc.exe bulunamadi, C++ kaynagindan derleniyor...'
    $msbuild = Get-MsBuildExe
    & $msbuild (Join-Path $root 'source\server\source\game\src\quest\qc.vcxproj') /t:Build /p:Configuration=Release /p:Platform=Win32 /v:minimal /nologo
    if ($LASTEXITCODE -ne 0) { throw "qc.exe build failed with code $LASTEXITCODE." }
}

$pyExe = (Get-Command python -ErrorAction SilentlyContinue).Source
if (!$pyExe) { throw 'Python bulunamadi!' }

Push-Location $questDir
try {
    Write-Host 'Quest dosyalari pre_qc.py ve qc.exe ile derleniyor...'
    & $pyExe 'pre_qc.py' -ac
    if ($LASTEXITCODE -ne 0) { throw "pre_qc.py failed with code $LASTEXITCODE." }

    $preQcDir = Join-Path $questDir 'pre_qc'
    if (Test-Path $preQcDir) { Remove-Item $preQcDir -Recurse -Force -ErrorAction SilentlyContinue }
} finally {
    Pop-Location
}

if ($serverWasRunning -and !$NoRestart) {
    Write-Host 'Oyun sunucusu yeni questlerle yeniden baslatiliyor...'
    & (Join-Path $PSScriptRoot 'start-server.ps1')
}

$sw.Stop()
Write-Host "Tum questler $([math]::Round($sw.Elapsed.TotalSeconds, 2)) saniyede basariyla derlendi!"
