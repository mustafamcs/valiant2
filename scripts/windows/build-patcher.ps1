# VALIANT2 AutoPatcher (VALIANT2.exe) derler, runtime + patch sunucusuna dagitir,
# self-update manifestini (patcher.json) UTF-8 BOM olmadan gunceller.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$settings = Ensure-ValidEnvForMachine
$root = $script:ProjectRoot
$patchRoot = Get-PatchRoot $settings
$baseUrl = Get-PublicBase $settings
$src = Join-Path $root 'source\patchserver\src'
$ico = Join-Path $root 'tools\branding\valiant2.ico'
$csc = Get-CscExe
Stop-BuildTargetProcesses -ProcessNames @('VALIANT2')

foreach ($d in @("$patchRoot\patcher", "$patchRoot\patch\files")) { New-Item -ItemType Directory -Force -Path $d | Out-Null }

$cfgSrc = Join-Path $env:TEMP 'PatcherCfg.cs'
$tempExe = Join-Path $env:TEMP 'VALIANT2_patcher_build.exe'
$utf8Bom = New-Object System.Text.UTF8Encoding($true)
$patcherCs = Join-Path $src 'Patcher.cs'
[System.IO.File]::WriteAllText($patcherCs, (Read-TextStripBom $patcherCs), $utf8Bom)
[System.IO.File]::WriteAllText($cfgSrc, "internal static class Cfg { public const string BASE_URL = `"$baseUrl`"; }", $utf8Bom)

& $csc /nologo /target:winexe /out:"$tempExe" /win32icon:"$ico" /res:"$src\logo.png" `
    /r:System.dll /r:System.Drawing.dll /r:System.Windows.Forms.dll /r:System.Net.dll /r:System.Runtime.Serialization.dll `
    $patcherCs $cfgSrc
if ($LASTEXITCODE -ne 0) { throw "Patcher derleme hatasi: $LASTEXITCODE" }

# Kaynak dosyayi tekrar BOM'suz UTF-8 yap (git diff temiz kalsin)
Write-Utf8NoBom $patcherCs (Read-TextStripBom $patcherCs)
Remove-Item "$patchRoot\src" -Recurse -Force -ErrorAction SilentlyContinue

Copy-Item $tempExe (Join-Path $root 'runtime\client\VALIANT2.exe') -Force
Copy-Item $tempExe (Join-Path $patchRoot 'patcher\VALIANT2.exe') -Force

$hash = (Get-FileHash $tempExe -Algorithm SHA256).Hash.ToLower()
Remove-Item $tempExe, $cfgSrc -Force -ErrorAction SilentlyContinue
$json = @{ version = 1; url = "$baseUrl/patcher/VALIANT2.exe"; sha256 = $hash } | ConvertTo-Json -Compress
Write-Utf8NoBom (Join-Path $patchRoot 'patch\patcher.json') $json
Write-Host "Patcher derlendi ve dagitildi. sha256: $hash"
