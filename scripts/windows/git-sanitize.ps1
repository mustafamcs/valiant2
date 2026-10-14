# .env'den uretilen runtime dosyalarini git degisikliklerinden gizler (skip-worktree).
# Tek toplu git cagrisi ile <0.1sn icinde tamamlanir.
. (Join-Path $PSScriptRoot 'common.ps1')
$root = $script:ProjectRoot
$git = Get-Command git.exe -ErrorAction SilentlyContinue
if (-not $git) { return }

Push-Location $root
try {
    $generated = @(
        'runtime/server/main/srv1/db/conf.txt',
        'web/adminpanel/start_panel.vbs'
    )
    foreach ($d in (Get-ServerCoreDirs)) {
        $cfg = Join-Path $d 'CONFIG'
        if (Test-Path $cfg -PathType Leaf) {
            $generated += ($cfg.Substring($root.Length + 1) -replace '\\','/')
        }
    }

    $tracked = @(& $git.Source ls-files -- $generated 2>$null)
    if ($tracked.Count -gt 0) {
        & $git.Source update-index --skip-worktree -- $tracked 2>$null
    }
} finally {
    Pop-Location
}
