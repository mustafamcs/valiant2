param([switch]$SkipPacks)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
if (!(Test-Path $vswhere)) { throw 'Visual Studio Build Tools 2022 is not installed.' }
$msbuild = & $vswhere -latest -products * -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1
if (!$msbuild) { throw 'MSBuild was not found.' }
$runtimeClient = Join-Path $root 'runtime\client'
@('UserData','mark','upload','logs','screenshot','syserr') | ForEach-Object { New-Item -ItemType Directory -Force -Path (Join-Path $runtimeClient $_) | Out-Null }
$langFile = Join-Path $runtimeClient 'UserData\lang.cfg'
$localeFile = Join-Path $runtimeClient 'UserData\loca.cfg'
if (!(Test-Path $langFile)) { Set-Content $langFile 'tr' -Encoding ascii -NoNewline }
if (!(Test-Path $localeFile)) { Set-Content $localeFile '1254 tr' -Encoding ascii -NoNewline }
& (Join-Path $PSScriptRoot 'sync-config.ps1')
& $msbuild (Join-Path $root 'source\client\Antrum_Client_Global.sln') /m /t:Build /p:Configuration=Release /p:Platform=Win32 /v:minimal
if ($LASTEXITCODE -ne 0) { throw "Client build failed with code $LASTEXITCODE." }
& $msbuild (Join-Path $root 'source\server\source\AntrumServer.sln') /m /t:Build /p:Configuration=Release /p:Platform=Win32 /v:minimal
if ($LASTEXITCODE -ne 0) { throw "Server build failed with code $LASTEXITCODE." }
if (!$SkipPacks) { & (Join-Path $PSScriptRoot 'build-client-packs.ps1') }
Write-Host 'All release targets built successfully.'
