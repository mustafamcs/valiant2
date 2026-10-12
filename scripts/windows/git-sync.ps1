# Pull -> yerel commit'leri uzakla esitle -> push.
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $root

git pull --rebase
if ($LASTEXITCODE -ne 0) { Write-Host "pull/rebase hatasi"; exit 1 }
git push
exit $LASTEXITCODE
