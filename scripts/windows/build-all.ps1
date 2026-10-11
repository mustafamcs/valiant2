param([switch]$SkipPacks)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
if (!(Test-Path $vswhere)) { throw 'Visual Studio Build Tools 2022 is not installed.' }
$msbuild = & $vswhere -latest -products * -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1
if (!$msbuild) { throw 'MSBuild was not found.' }
& (Join-Path $PSScriptRoot 'sync-config.ps1')
& $msbuild (Join-Path $root 'source\client\Antrum_Client_Global.sln') /m /t:Build /p:Configuration=Release /p:Platform=Win32 /v:minimal
if ($LASTEXITCODE -ne 0) { throw "Client build failed with code $LASTEXITCODE." }
& $msbuild (Join-Path $root 'source\server\source\AntrumServer.sln') /m /t:Build /p:Configuration=Release /p:Platform=Win32 /v:minimal
if ($LASTEXITCODE -ne 0) { throw "Server build failed with code $LASTEXITCODE." }
if (!$SkipPacks) { & (Join-Path $PSScriptRoot 'build-client-packs.ps1') }
Write-Host 'All release targets built successfully.'
