$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$stateDir = Join-Path $root 'runtime\server\.state'
if (!(Test-Path $stateDir)) { Write-Host 'No server state found.'; return }
Get-ChildItem $stateDir -File -Filter '*.pid' | ForEach-Object {
    $processId = [int](Get-Content $_.FullName | Select-Object -First 1)
    $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
    [pscustomobject]@{ Component=$_.BaseName; PID=$processId; Status=$(if($process){'Running'}else{'Stopped'}) }
} | Format-Table -AutoSize
