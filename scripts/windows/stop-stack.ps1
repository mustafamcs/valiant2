# Web/patch altyapisini durdurur (oyun sunucusuna dokunmaz -> stop-server.cmd)
$procs = Get-CimInstance Win32_Process | Where-Object {
    ($_.Name -match '^(php|python|pythonw)\.exe$' -and $_.CommandLine -match 'router\.php|file_server\.py|patch_watch\.py') -or
    $_.Name -eq 'nginx.exe'
}
foreach ($p in $procs) { Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue; Write-Host "Durduruldu: $($p.Name) (PID $($p.ProcessId))" }
Write-Host 'Stack durduruldu.'
