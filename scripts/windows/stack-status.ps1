# Tum servislerin saglik durumu: oyun portlari, panel, patch, nginx, izleyici.
$results = @()
$tcp = {
    param($name, $port)
    $open = [bool](Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue)
    [pscustomobject]@{ Servis = $name; Hedef = "port $port"; Durum = $(if ($open) { 'ACIK' } else { 'KAPALI' }) }
}
$http = {
    param($name, $url)
    $code = & curl.exe -sk -o NUL -w "%{http_code}" --max-time 5 $url 2>$null
    [pscustomobject]@{ Servis = $name; Hedef = $url; Durum = $(if ($code -and $code -ne '000') { "HTTP $code" } else { 'ULASILAMIYOR' }) }
}
$results += & $tcp 'MariaDB' 3306
$results += & $tcp 'Auth (oyun)' 30001
$results += & $tcp 'CH1 core1' 30003
$results += & $tcp 'CH1 core2' 30005
$results += & $tcp 'CH1 core3' 30007
$results += & $tcp 'CH1 core4' 30009
$results += & $tcp 'CH99' 30051
$results += & $tcp 'P2P auth' 30002
$results += & $tcp 'DB peer' 30000
$results += & $http 'Panel' 'https://213.254.136.100/'
$results += & $http 'Patch manifest' 'https://213.254.136.100/update/patchlist.json'
$results += & $http 'Patcher exe' 'https://213.254.136.100/patcher/VALIANT2.exe'
$nginx = Get-Process nginx -ErrorAction SilentlyContinue
$results += [pscustomobject]@{ Servis = 'nginx'; Hedef = '443/80'; Durum = $(if ($nginx) { "Calisiyor ($($nginx.Count) proc)" } else { 'KAPALI' }) }
$pw = Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" | Where-Object { $_.CommandLine -match 'patch_watch' }
$results += [pscustomobject]@{ Servis = 'Patch watcher'; Hedef = 'patch_watch.py'; Durum = $(if ($pw) { 'Calisiyor' } else { 'KAPALI' }) }
$fs = Get-NetTCPConnection -LocalPort 8091 -State Listen -ErrorAction SilentlyContinue
$results += [pscustomobject]@{ Servis = 'Dosya sunucusu'; Hedef = 'port 8091'; Durum = $(if ($fs) { 'ACIK' } else { 'KAPALI' }) }
$results | Format-Table -AutoSize
