param([string]$Archive = 'all')
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Get-Process -Name 'M2Client' -ErrorAction SilentlyContinue | Stop-Process -Force
$assets = Join-Path $root 'assets\unpacked'
$archiver = Join-Path $assets 'FSArchiver.exe'
$runtimePack = Join-Path $root 'runtime\client\pack'
New-Item -ItemType Directory -Force -Path $runtimePack | Out-Null
Push-Location $assets
try {
    & $archiver 'config.json' $Archive
    if ($LASTEXITCODE -ne 0) { throw "FSArchiver failed with code $LASTEXITCODE." }
} finally {
    Pop-Location
}
Write-Host 'Client packs built.'
