# VALIANT2 AutoPatcher (VALIANT2.exe) derler, runtime + patch sunucusuna dagitir,
# self-update manifestini (patcher.json) gunceller.
# Kaynak: <repo>\source\patchserver\src\Patcher.cs — BASE_URL derleme aninda .env'den uretilen Cfg sinifindan gelir.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$settings = Get-EnvSettings
$root = $script:ProjectRoot
$patchRoot = Get-PatchRoot $settings
$baseUrl = Get-PublicBase $settings
$src = Join-Path $root 'source\patchserver\src'
$csc = 'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe'

foreach ($d in @("$patchRoot\patcher", "$patchRoot\patch\files")) { New-Item -ItemType Directory -Force -Path $d | Out-Null }

# Canli BASE_URL'i iceren Cfg sinifini derleme aninda uret (kaynak dosya degismez)
$cfgSrc = Join-Path $env:TEMP 'PatcherCfg.cs'
"internal static class Cfg { public const string BASE_URL = `"$baseUrl`"; }" | Set-Content $cfgSrc -Encoding UTF8

& $csc /nologo /target:winexe /out:"$src\VALIANT2.exe" /win32icon:"$src\valiant2.ico" /res:"$src\logo.png" `
    /r:System.dll /r:System.Drawing.dll /r:System.Windows.Forms.dll /r:System.Net.dll /r:System.Runtime.Serialization.dll `
    (Join-Path $src 'Patcher.cs') $cfgSrc
if ($LASTEXITCODE -ne 0) { throw "Patcher derleme hatasi: $LASTEXITCODE" }

Copy-Item "$src\VALIANT2.exe" (Join-Path $root 'runtime\client\VALIANT2.exe') -Force
Copy-Item "$src\VALIANT2.exe" (Join-Path $patchRoot 'patcher\VALIANT2.exe') -Force

$hash = (Get-FileHash "$src\VALIANT2.exe" -Algorithm SHA256).Hash.ToLower()
$json = @{ version = 1; url = "$baseUrl/patcher/VALIANT2.exe"; sha256 = $hash } | ConvertTo-Json -Compress
Set-Content -Path (Join-Path $patchRoot 'patch\patcher.json') -Value $json -Encoding ascii
Write-Host "Patcher derlendi ve dagitildi. sha256: $hash"
