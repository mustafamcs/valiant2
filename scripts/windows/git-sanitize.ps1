# .env'den uretilen runtime dosyalarini git degisikliklerinden gizler (skip-worktree).
# Bu dosyalar her makinede yeniden uretildigi icin diff olarak cikmamalidir.
# sync-config.ps1 ve setup.ps1 bunu otomatik cagirir.
. (Join-Path $PSScriptRoot 'common.ps1')
$root = $script:ProjectRoot
$git = Get-Command git.exe -ErrorAction SilentlyContinue
if (-not $git) { return }  # git yoksa sessizce gec

Set-Location $root
$generated = @(
    'runtime/server/main/srv1/db/conf.txt',
    'web/adminpanel/start_panel.vbs'
)
$generated += Get-ChildItem (Join-Path $root 'runtime\server') -Recurse -File -Filter CONFIG -ErrorAction SilentlyContinue |
    ForEach-Object { $_.FullName.Substring($root.Length + 1) -replace '\\','/' }

foreach ($f in $generated) {
    & $git.Source update-index --skip-worktree $f 2>$null
}
