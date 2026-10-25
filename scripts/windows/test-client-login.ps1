param([switch]$KeepOpen, [switch]$TestCharChange)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
. (Join-Path $PSScriptRoot 'common.ps1')

Stop-ClientProcesses
$gameDir = Join-Path $root 'runtime\client\game'
$syserrDir = Join-Path $gameDir 'syserr'
Remove-Item (Join-Path $syserrDir '*.txt') -Force -ErrorAction SilentlyContinue

Set-Content -Path (Join-Path $gameDir 'autologin.cfg') -Value '1' -Encoding ascii -NoNewline
if ($TestCharChange) {
    Set-Content -Path (Join-Path $gameDir 'autochange.cfg') -Value '1' -Encoding ascii -NoNewline
}
Write-Host 'M2Client.exe otomatik giris (Login -> Karakter Secimi -> Harita Yukleme -> Oyun Ici) baslatiliyor...' -ForegroundColor Cyan
$proc = Start-Process -FilePath (Join-Path $gameDir 'bin\M2Client.exe') -WorkingDirectory $gameDir -PassThru

$enteredGame = $false
for ($i = 0; $i -lt 24; $i++) {
    Start-Sleep -Milliseconds 500
    if ($proc.HasExited) { break }
    $logTail = Get-Content (Join-Path $root 'runtime\server\main\srv1\chan\ch1\core1\syslog.txt') -Tail 15 -ErrorAction SilentlyContinue
    if ($logTail -match 'P2P: Login') {
        $enteredGame = $true
    }
}
Start-Sleep -Seconds 3
if ($TestCharChange) {
    Write-Host 'Karakter degistirme testi: 15sn bekleniyor (autochange.cfg -> net.ExitGame -> login fazi)...' -ForegroundColor Cyan
    for ($i = 0; $i -lt 15; $i++) {
        Start-Sleep -Seconds 1
        if ($proc.HasExited) { break }
    }
}
$running = !$proc.HasExited
$title = if ($running) { (Get-Process -Id $proc.Id -ErrorAction SilentlyContinue).MainWindowTitle } else { 'EXITED' }
Write-Host ("Durum: ClientRunning={0} | WindowTitle='{1}' | ServerLogin={2}" -f $running, $title, $enteredGame) -ForegroundColor $(if ($running -and $title -ne 'LOG') { 'Green' } else { 'Red' })

$latest = Get-ChildItem (Join-Path $syserrDir '*.txt') -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($latest) {
    Write-Host ("=== CLIENT SYSERR ({0}, {1} bytes) ===" -f $latest.Name, $latest.Length) -ForegroundColor Yellow
    Get-Content $latest.FullName
}
Remove-Item (Join-Path $gameDir 'autologin.cfg') -Force -ErrorAction SilentlyContinue
if (-not $KeepOpen -and $running) {
    Stop-ClientProcesses
}