# Degisiklikleri sahnele + commit at. Kullanim: git-save.cmd "mesaj"
# Mesaj verilmezse tarihli otomatik mesaj atilir.
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $root

git status --short
if (-not (git status --porcelain)) {
    Write-Host "Commit edilecek degisiklik yok."
    exit 0
}

$msg = if ($args) { $args -join ' ' } else { "update $(Get-Date -Format 'yyyy-MM-dd HH:mm')" }
git add -A
git commit -m $msg -m "Generated with Devin" | Write-Host
Write-Host "Commit atildi: $msg"
