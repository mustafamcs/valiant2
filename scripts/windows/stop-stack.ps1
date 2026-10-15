# Web/patch altyapisini durdurur (oyun sunucusuna dokunmaz -> stop-server.cmd)
$procs = @(Get-CimInstance Win32_Process | Where-Object {
    ($_.Name -match '^(php|python|pythonw)\.exe$' -and $_.CommandLine -match 'router\.php|file_server\.py|patch_watch\.py') -or
    $_.Name -eq 'nginx.exe'
})
$failedIds = @()
foreach ($p in $procs) {
    try {
        Stop-Process -Id $p.ProcessId -Force -ErrorAction Stop
        Write-Host "Durduruldu: $($p.Name) (PID $($p.ProcessId))"
    } catch {
        $failedIds += $p.ProcessId
    }
}
if ($failedIds.Count -gt 0) {
    $pidArgs = ($failedIds | ForEach-Object { "/PID $_" }) -join ' '
    try {
        Start-Process -FilePath 'taskkill.exe' -ArgumentList "/F $pidArgs" -Verb RunAs -WindowStyle Hidden -Wait -ErrorAction SilentlyContinue
    } catch {}
}
Write-Host 'Stack durduruldu.'
