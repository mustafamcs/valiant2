# Tum web/patch altyapisini arka planda baslatir: nginx + 4 PHP worker + dosya sunucusu + patch watcher.
# Oyun sunucusu icin: start-server.cmd
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$panel = Join-Path $root 'web\adminpanel'
$php = 'C:\Users\Administrator\AppData\Local\Microsoft\WinGet\Packages\PHP.PHP.8.3_Microsoft.Winget.Source_8wekyb3d8bbwe\php.exe'
$pythonw = 'C:\Program Files\Python312\pythonw.exe'

# PHP panel worker'lari (nginx upstream: 8090,8092,8093,8094)
foreach ($port in 8090,8092,8093,8094) {
    $listening = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if (-not $listening) {
        $vbs = Join-Path $panel 'start_panel.vbs'
        Start-Process -FilePath 'wscript.exe' -ArgumentList ('"{0}"' -f $vbs) -WorkingDirectory $panel
        break
    }
}
# Nginx
if (-not (Get-Process nginx -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath 'C:\nginx-1.27.5\nginx.exe' -WorkingDirectory 'C:\nginx-1.27.5' -WindowStyle Hidden
}
# Patch dosya sunucusu (127.0.0.1:8091)
if (-not (Get-NetTCPConnection -LocalPort 8091 -State Listen -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath $pythonw -ArgumentList 'C:\patchserver\file_server.py' -WindowStyle Hidden
}
# Patch watcher (runtime/client/game -> patch/files senkronu)
if (-not (Get-Process pythonw -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'patch_watch' })) {
    $running = Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" | Where-Object { $_.CommandLine -match 'patch_watch' }
    if (-not $running) { Start-Process -FilePath $pythonw -ArgumentList 'C:\patchserver\patch_watch.py' -WindowStyle Hidden }
}
Start-Sleep -Seconds 2
& (Join-Path $PSScriptRoot 'stack-status.ps1')
