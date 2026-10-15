$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
. (Join-Path $PSScriptRoot 'common.ps1')
$stateDir = Join-Path $root 'runtime\server\.state'
Stop-ServerProcesses
if (Test-Path $stateDir) {
    Get-ChildItem $stateDir -File -Filter '*.pid' -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
}
& (Join-Path $PSScriptRoot 'protect-config.ps1')
Write-Host 'Oyun sunucusu aninda durduruldu.'
