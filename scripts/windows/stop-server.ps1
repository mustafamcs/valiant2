$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$stateDir = Join-Path $root 'runtime\server\.state'
if (!(Test-Path $stateDir)) { return }
Get-ChildItem $stateDir -File -Filter '*.pid' | ForEach-Object {
    $processId = [int](Get-Content $_.FullName | Select-Object -First 1)
    $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
    if ($process) {
        Stop-Process -Id $processId
        $null = $process.WaitForExit(10000)
        Write-Host "$($_.BaseName) stopped."
    }
    Remove-Item $_.FullName -Force
}
& (Join-Path $PSScriptRoot 'protect-config.ps1')
