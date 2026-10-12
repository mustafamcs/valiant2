# Tum web/patch altyapisini arka planda baslatir: nginx + 4 PHP worker + dosya sunucusu + patch watcher.
# Oyun sunucusu icin: start-server.cmd
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$settings = Get-EnvSettings
$root = $script:ProjectRoot
$panel = Join-Path $root 'web\adminpanel'
$patchRoot = Get-PatchRoot $settings

# --- PHP panel worker'lari (nginx upstream: 8090,8092,8093,8094) ---
# start_panel.vbs'i her seferinde guncel uret (php yolu makineye gore degisebilir)
$php = Get-PhpExe
$vbs = Join-Path $panel 'start_panel.vbs'
$phpEsc = $php -replace '"', ''
$vbsContent = @"
Set sh = CreateObject("WScript.Shell")
q = Chr(34)
php = "$phpEsc"
dirp = "$panel"
ports = Array(8090, 8092, 8093, 8094)
For Each p In ports
    sh.Run "cmd /c cd /d " & q & dirp & q & " && " & q & php & q & " -d display_errors=0 -S 127.0.0.1:" & p & " router.php", 0, False
Next
"@
Set-Content $vbs $vbsContent -Encoding ASCII

$needPanel = $false
foreach ($port in 8090,8092,8093,8094) {
    if (-not (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue)) { $needPanel = $true; break }
}
if ($needPanel) {
    Start-Process -FilePath 'wscript.exe' -ArgumentList ('"{0}"' -f $vbs) -WorkingDirectory $panel
}

# --- Nginx ---
if (-not (Get-Process nginx -ErrorAction SilentlyContinue)) {
    $nginx = Get-NginxExe
    if ($nginx) {
        Start-Process -FilePath $nginx -WorkingDirectory (Split-Path $nginx) -WindowStyle Hidden
    } else { Write-Host 'UYARI: nginx bulunamadi (setup.cmd calistirilmali)' }
}

# --- Patch altyapisi ---
$pythonw = Get-PythonwExe
$patchScripts = Join-Path $root 'source\patchserver'
New-Item -ItemType Directory -Force -Path "$patchRoot\patch\files", "$patchRoot\patcher" | Out-Null

# Dosya sunucusu ve watcher'i patchRoot'a kur (guncel kaynaktan)
foreach ($f in 'file_server.py','patch_watch.py') {
    $dst = Join-Path $patchRoot $f
    Copy-Item (Join-Path $patchScripts $f) $dst -Force
}
# patchserver.json yoksa uret
$cfgFile = Join-Path $patchRoot 'patchserver.json'
if (-not (Test-Path $cfgFile)) {
    @{
        game_dir = (Join-Path $root 'runtime\client\game')
        patch_dir = "$patchRoot\patch"
        patcher_dir = "$patchRoot\patcher"
        base_url = (Get-PublicBase $settings)
    } | ConvertTo-Json | Set-Content $cfgFile -Encoding ascii
    Write-Host "patchserver.json uretildi: $cfgFile"
}

if (-not (Get-NetTCPConnection -LocalPort 8091 -State Listen -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath $pythonw -ArgumentList ('"{0}"' -f (Join-Path $patchRoot 'file_server.py')) -WindowStyle Hidden
}
$watcher = Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" | Where-Object { $_.CommandLine -match 'patch_watch' }
if (-not $watcher) {
    Start-Process -FilePath $pythonw -ArgumentList ('"{0}"' -f (Join-Path $patchRoot 'patch_watch.py')) -WindowStyle Hidden
}

Start-Sleep -Seconds 2
& (Join-Path $PSScriptRoot 'stack-status.ps1')
