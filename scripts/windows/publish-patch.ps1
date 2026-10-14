# Patch manifestini onbellekli (hashcache.json) olarak hiper-hizli uretir ve versiyonu +1 artirir.
# Tum JSON dosyalarini UTF-8 BOM olmadan yazar.
$ErrorActionPreference = 'Stop'
$sw = [Diagnostics.Stopwatch]::StartNew()
. (Join-Path $PSScriptRoot 'common.ps1')
$settings = Ensure-ValidEnvForMachine
$patchDir = Join-Path (Get-PatchRoot $settings) 'patch'
$filesDir = Join-Path $patchDir 'files'
$listFile = Join-Path $patchDir 'patchlist.json'
$cacheFile = Join-Path $patchDir 'hashcache.json'
$baseUrl = Get-PublicBase $settings

New-Item -ItemType Directory -Force -Path $filesDir | Out-Null

$cache = @{}
if (Test-Path $cacheFile) {
    try {
        $rawCache = (Read-TextStripBom $cacheFile) | ConvertFrom-Json
        foreach ($p in $rawCache.PSObject.Properties) {
            $cache[$p.Name] = $p.Value
        }
    } catch {}
}

$newCache = @{}
$entries = @(Get-ChildItem $filesDir -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($filesDir.Length + 1) -replace '\\', '/'
    $key = "$rel|$($_.Length)|$($_.LastWriteTimeUtc.Ticks)"
    $hash = $null
    if ($cache.ContainsKey($key)) {
        $hash = $cache[$key]
    } else {
        $hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower()
    }
    $newCache[$key] = $hash
    [pscustomobject]@{ path = $rel; size = $_.Length; sha256 = $hash }
} | Sort-Object path)

Write-Utf8NoBom $cacheFile ($newCache | ConvertTo-Json -Compress)

$ver = 0
if (Test-Path $listFile) {
    try { $ver = [int](((Read-TextStripBom $listFile) | ConvertFrom-Json).version) } catch {}
}
$manifest = @{ version = $ver + 1; base = "$baseUrl/update/files/"; files = $entries }
Write-Utf8NoBom $listFile ($manifest | ConvertTo-Json -Depth 4)
$sw.Stop()
$el = [math]::Round($sw.Elapsed.TotalSeconds, 2)
Write-Host "Manifest v$($ver + 1) yayinlandi ($($entries.Count) dosya, $el sn)."
