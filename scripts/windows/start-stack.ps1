# Tum web/patch altyapisini arka planda hiper-hizli baslatir: nginx + 4 PHP worker + dosya sunucusu + patch watcher.
# VBScript (ANSI/BOM) bagimliligi olmadan dogrudan Unicode uyumlu Start-Process kullanir.
$ErrorActionPreference = 'Stop'
$sw = [Diagnostics.Stopwatch]::StartNew()
. (Join-Path $PSScriptRoot 'common.ps1')
$hw = Optimize-HardwareConfig
$settings = Ensure-ValidEnvForMachine
$root = $script:ProjectRoot
$panel = Join-Path $root 'web\adminpanel'
$patchRoot = Get-PatchRoot $settings

# --- PHP panel worker'lari (nginx upstream: 8090,8092,8093,8094) ---
$php = Get-PhpExe
$listeningPorts = @([Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners() | ForEach-Object { $_.Port })

foreach ($port in 8090,8092,8093,8094) {
    if ($listeningPorts -notcontains $port) {
        Start-Process -FilePath $php -ArgumentList "-d display_errors=0 -d opcache.enable_cli=1 -S 127.0.0.1:$port router.php" -WorkingDirectory $panel -WindowStyle Hidden
    }
}

# --- Nginx ---
if (-not (Get-Process nginx -ErrorAction SilentlyContinue)) {
    $nginx = Get-NginxExe
    if ($nginx) {
        Remove-FileBomIfPresent (Join-Path (Split-Path $nginx) 'conf\nginx.conf') | Out-Null
        Start-Process -FilePath $nginx -WorkingDirectory (Split-Path $nginx) -WindowStyle Hidden
    } else { Write-Host 'UYARI: nginx bulunamadi (setup.cmd calistirilmali)' }
}

# --- Patch altyapisi ---
$pythonw = Get-PythonwExe
$patchScripts = Join-Path $root 'source\patchserver'
New-Item -ItemType Directory -Force -Path "$patchRoot\patch\files", "$patchRoot\patcher" | Out-Null

foreach ($f in 'file_server.py','patch_watch.py') {
    Copy-Item (Join-Path $patchScripts $f) (Join-Path $patchRoot $f) -Force
}
$cfgFile = Join-Path $patchRoot 'patchserver.json'
$newCfgJson = @{
    game_dir    = (Join-Path $root 'runtime\client\game')
    patch_dir   = "$patchRoot\patch"
    patcher_dir = "$patchRoot\patcher"
    base_url    = (Get-PublicBase $settings)
} | ConvertTo-Json
Write-Utf8NoBom $cfgFile $newCfgJson

if ($listeningPorts -notcontains 8091) {
    Start-Process -FilePath $pythonw -ArgumentList ('"{0}"' -f (Join-Path $patchRoot 'file_server.py')) -WorkingDirectory $patchRoot -WindowStyle Hidden
}
$watcher = Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'patch_watch' }
if (-not $watcher) {
    Start-Process -FilePath $pythonw -ArgumentList ('"{0}"' -f (Join-Path $patchRoot 'patch_watch.py')) -WorkingDirectory $patchRoot -WindowStyle Hidden
}

for ($i = 0; $i -lt 40; $i++) {
    $curPorts = @([Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners() | ForEach-Object { $_.Port })
    if (($curPorts -contains 8090) -and ($curPorts -contains 8091)) { break }
    Start-Sleep -Milliseconds 50
}

$sw.Stop()
$el = [math]::Round($sw.Elapsed.TotalSeconds, 2)
Write-Host "Web & Patch Stack $el saniyede hazir!"
& (Join-Path $PSScriptRoot 'stack-status.ps1')
