$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$stateDir = Join-Path $root 'runtime\server\.state'
Get-Process -Name 'game','db' -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
if (Test-Path $stateDir) {
    Get-ChildItem $stateDir -File -Filter '*.pid' -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
}
& (Join-Path $PSScriptRoot 'protect-config.ps1')
Write-Host 'Oyun sunucusu aninda durduruldu.'
