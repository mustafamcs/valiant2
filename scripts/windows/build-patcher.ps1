# VALIANT2 AutoPatcher (VALIANT2.exe) derler, runtime + patch sunucusuna dagitir,
# self-update manifestini (patcher.json) gunceller.
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$patchRoot = 'C:\patchserver'
$src = Join-Path $patchRoot 'src'
$csc = 'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe'

& $csc /nologo /target:winexe /out:"$src\VALIANT2.exe" /win32icon:"$src\valiant2.ico" /res:"$src\logo.png" `
    /r:System.dll /r:System.Drawing.dll /r:System.Windows.Forms.dll /r:System.Net.dll /r:System.Runtime.Serialization.dll `
    (Join-Path $src 'Patcher.cs')
if ($LASTEXITCODE -ne 0) { throw "Patcher derleme hatasi: $LASTEXITCODE" }

Copy-Item "$src\VALIANT2.exe" (Join-Path $root 'runtime\client\VALIANT2.exe') -Force
Copy-Item "$src\VALIANT2.exe" (Join-Path $patchRoot 'patcher\VALIANT2.exe') -Force

$hash = (Get-FileHash "$src\VALIANT2.exe" -Algorithm SHA256).Hash.ToLower()
$json = @{ version = 1; url = 'https://213.254.136.100/patcher/VALIANT2.exe'; sha256 = $hash } | ConvertTo-Json -Compress
Set-Content -Path (Join-Path $patchRoot 'patch\patcher.json') -Value $json -Encoding ascii
Write-Host "Patcher derlendi ve dagitildi. sha256: $hash"
