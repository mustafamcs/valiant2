# Patch manifest'ini elle yeniden uretir ve versiyonu +1 artirir.
# Not: patch_watch.py bunu otomatik yapar; bu script acil/elle yayin icin.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$settings = Get-EnvSettings
$patchDir = Join-Path (Get-PatchRoot $settings) 'patch'
$filesDir = Join-Path $patchDir 'files'
$listFile = Join-Path $patchDir 'patchlist.json'
$baseUrl = Get-PublicBase $settings

$entries = Get-ChildItem $filesDir -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($filesDir.Length + 1) -replace '\\', '/'
    [pscustomobject]@{ path = $rel; size = $_.Length; sha256 = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower() }
} | Sort-Object path

$ver = 0
if (Test-Path $listFile) { $ver = [int]((Get-Content $listFile -Raw | ConvertFrom-Json).version) }
$manifest = @{ version = $ver + 1; base = "$baseUrl/update/files/"; files = $entries }
$manifest | ConvertTo-Json -Depth 4 | Set-Content $listFile -Encoding ascii
Write-Host "Manifest v$($ver + 1) yayinlandi ($($entries.Count) dosya)."
