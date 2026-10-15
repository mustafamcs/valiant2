param([switch]$SkipPacks, [switch]$ForcePacks)
$ErrorActionPreference = 'Stop'
$sw = [Diagnostics.Stopwatch]::StartNew()
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
. (Join-Path $PSScriptRoot 'common.ps1')
$hw = Optimize-HardwareConfig
$threads = $hw.MsBuildThreads
$msbuild = Get-MsBuildExe

Write-Host "Hiper-Hizli Derleme Modu Aktif: $($hw.CpuName) ($($hw.Cores) Cekirdek / $threads Thread, $($hw.RamGb) GB RAM)"

$runtimeClient = Join-Path $root 'runtime\client\game'
@('UserData','mark','upload','logs','screenshot','syserr') | ForEach-Object { New-Item -ItemType Directory -Force -Path (Join-Path $runtimeClient $_) | Out-Null }
$langFile = Join-Path $runtimeClient 'UserData\lang.cfg'
$localeFile = Join-Path $runtimeClient 'UserData\loca.cfg'
if (!(Test-Path $langFile)) { Set-Content $langFile 'tr' -Encoding ascii -NoNewline }
if (!(Test-Path $localeFile)) { Set-Content $localeFile '1254 tr' -Encoding ascii -NoNewline }
$channelFile = Join-Path $runtimeClient 'channel.inf'
if (!(Test-Path $channelFile)) { Set-Content $channelFile '1 0 0' -Encoding ascii -NoNewline }

& (Join-Path $PSScriptRoot 'sync-config.ps1')

$env:CL = "/MP$threads"
$msbCommon = @("/m:$threads", "/p:CL_MPCount=$threads", "/p:UseMultiToolTask=true", "/p:EnforceProcessCountAcrossBuilds=true", "/v:minimal", "/nologo")

& $msbuild (Join-Path $root 'tools\client-config\Valiant2Config.csproj') /t:Build /p:Configuration=Release /p:Platform=AnyCPU @msbCommon
if ($LASTEXITCODE -ne 0) { throw "Config build failed with code $LASTEXITCODE." }

& $msbuild (Join-Path $root 'source\client\Antrum_Client_Global.sln') /t:Build /p:Configuration=Release /p:Platform=Win32 @msbCommon
if ($LASTEXITCODE -ne 0) { throw "Client build failed with code $LASTEXITCODE." }

& $msbuild (Join-Path $root 'tools\client-launcher\Valiant2Launcher.csproj') /t:Build /p:Configuration=Release /p:Platform=AnyCPU @msbCommon
if ($LASTEXITCODE -ne 0) { throw "Launcher build failed with code $LASTEXITCODE." }

# Eger oyun sunucusu calisiyorsa game.exe / db.exe kilitli olmamasi icin gecici durdur, bitince otomatik baslat
$serverWasRunning = [bool](Get-Process -Name 'game','db' -ErrorAction SilentlyContinue)
if ($serverWasRunning) {
    Write-Host 'Calisan sunucu derleme icin gecici durduruluyor...'
    Stop-ServerProcesses
}

& $msbuild (Join-Path $root 'source\server\source\AntrumServer.sln') /t:Build /p:Configuration=Release /p:Platform=Win32 @msbCommon
if ($LASTEXITCODE -ne 0) { throw "Server build failed with code $LASTEXITCODE." }

if ($serverWasRunning) {
    Write-Host 'Sunucu yeni derlenen ikililerle yeniden baslatiliyor...'
    & (Join-Path $PSScriptRoot 'start-server.ps1')
}

& (Join-Path $PSScriptRoot 'build-control-center.ps1')
& (Join-Path $PSScriptRoot 'build-patcher.ps1')

if (!$SkipPacks) {
    if ($ForcePacks) {
        & (Join-Path $PSScriptRoot 'build-client-packs.ps1') -Force
    } else {
        & (Join-Path $PSScriptRoot 'build-client-packs.ps1')
    }
}

$sw.Stop()
Write-Host "Tum hedefler $([math]::Round($sw.Elapsed.TotalSeconds, 2)) saniyede basariyla derlendi!"
