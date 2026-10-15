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
        'assets/unpacked/data/root/serverinfo.py',
        'source/client/external/projects/CRootLib/Workplace/__cython/root_modules/serverinfo.py'
    )
    foreach ($d in (Get-ServerCoreDirs)) {
        $cfg = Join-Path $d 'CONFIG'
        if (Test-Path $cfg -PathType Leaf) {
            $generated += ($cfg.Substring($root.Length + 1) -replace '\\','/')
        }
    }
    $monsterDir = Join-Path $root 'runtime\server\main\srv1\share\data\monster'
    if (Test-Path $monsterDir) {
        Get-ChildItem $monsterDir -Force -ErrorAction SilentlyContinue | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint } | ForEach-Object {
            $generated += "runtime/server/main/srv1/share/data/monster/$($_.Name)"
        }
    }

    $tracked = @(& $git.Source ls-files -- $generated 2>$null)
    if ($tracked.Count -gt 0) {
        for ($i = 0; $i -lt $tracked.Count; $i += 150) {
            $end = [Math]::Min($i + 149, $tracked.Count - 1)
            $batch = $tracked[$i..$end]
            & $git.Source update-index --skip-worktree -- $batch 2>$null
        }
    }
} finally {
    Pop-Location
}
