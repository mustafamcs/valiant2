# Ortak yardimcilar - tum scriptler buradan .env okur, araclari bulur, UTF-8 BOM onarimi ve donanim optimizasyonu yapar.
# Kullanim: . (Join-Path $PSScriptRoot 'common.ps1')

$script:ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$script:Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Write-Utf8NoBom {
    param([string]$Path, [string]$Content)
    $dir = Split-Path -Parent $Path
    if ($dir -and -not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    [System.IO.File]::WriteAllText($Path, $Content, $script:Utf8NoBom)
}

function Read-TextStripBom {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return '' }
    $txt = [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)
    if ($txt.Length -gt 0 -and [int][char]$txt[0] -eq 0xFEFF) {
        $txt = $txt.Substring(1)
    }
    return $txt
}

function Remove-FileBomIfPresent {
    param([string]$Path)
    if (-not (Test-Path $Path -PathType Leaf)) { return $false }
    try {
        $bytes = [System.IO.File]::ReadAllBytes($Path)
        if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
            $newBytes = New-Object byte[] ($bytes.Length - 3)
            [System.Array]::Copy($bytes, 3, $newBytes, 0, $newBytes.Length)
            [System.IO.File]::WriteAllBytes($Path, $newBytes)
            return $true
        }
    } catch {}
    return $false
}

function Get-ServerCoreDirs {
    $srvRoot = Join-Path $script:ProjectRoot 'runtime\server\main\srv1'
    $dirs = @(
        (Join-Path $srvRoot 'auth'),
        (Join-Path $srvRoot 'db'),
        (Join-Path $srvRoot 'share\conf')
    )
    $chanDir = Join-Path $srvRoot 'chan'
    if (Test-Path $chanDir) {
        $dirs += Get-ChildItem $chanDir -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            Get-ChildItem $_.FullName -Directory -Filter 'core*' -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName
        }
    }
    return $dirs
}

function Repair-AllBomFiles {
    $root = $script:ProjectRoot
    $targets = @(
        (Join-Path $root '.env'),
        (Join-Path $root 'runtime\dependencies\nginx\conf\nginx.conf'),
        (Join-Path $root 'runtime\dependencies\mariadb\data\my.ini'),
        (Join-Path $root 'runtime\patchserver\patchserver.json'),
        (Join-Path $root 'runtime\patchserver\patch\patchlist.json'),
        (Join-Path $root 'runtime\patchserver\patch\patcher.json'),
        (Join-Path $root 'runtime\patchserver\patch\hashcache.json'),
        (Join-Path $root 'assets\unpacked\data\root\serverinfo.py'),
        (Join-Path $root 'source\client\external\projects\CRootLib\Workplace\__cython\root_modules\serverinfo.py')
    )
    foreach ($d in (Get-ServerCoreDirs)) {
        foreach ($name in 'CONFIG','conf.txt','CMD','CRC','VERSION','BANIP') {
            $p = Join-Path $d $name
            if (Test-Path $p -PathType Leaf) { $targets += $p }
        }
    }
    $targets += Get-ChildItem (Join-Path $root 'scripts\windows') -File -Include '*.ps1','*.cmd','*.py' -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName
    $targets += Get-ChildItem (Join-Path $root 'assets\unpacked') -File -Filter '*.bat' -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName
    foreach ($t in $targets) {
        Remove-FileBomIfPresent $t | Out-Null
    }
}

function Get-LocalAdapterIps {
    $ips = @()
    try {
        $ips = @(Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
            Where-Object { $_.IPAddress -notmatch '^(127\.|169\.254\.)' -and $_.PrefixOrigin -ne 'WellKnown' } |
            Select-Object -ExpandProperty IPAddress)
    } catch {}
    if ($ips.Count -eq 0) {
        try {
            $ips = @([Net.Dns]::GetHostAddresses([Net.Dns]::GetHostName()) |
                Where-Object { $_.AddressFamily -eq 'InterNetwork' -and $_.IPAddressToString -notmatch '^(127\.|169\.254\.)' } |
                ForEach-Object { $_.IPAddressToString })
        } catch {}
    }
    return $ips
}

function Get-ExternalWanIp {
    if ($script:CachedWanIp) { return $script:CachedWanIp }
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    foreach ($svc in 'https://api.ipify.org','https://ifconfig.me/ip','https://icanhazip.com') {
        try {
            $ip = (Invoke-WebRequest $svc -UseBasicParsing -TimeoutSec 3).Content.Trim()
            if ($ip -match '^\d{1,3}(\.\d{1,3}){3}$') {
                $script:CachedWanIp = $ip
                return $ip
            }
        } catch {}
    }
    return $null
}

function Test-IpReachableOnThisMachine {
    param([string]$TestIp)
    if ([string]::IsNullOrWhiteSpace($TestIp)) { return $false }
    if ($TestIp -eq '127.0.0.1') { return $true }
    $localIps = @(Get-LocalAdapterIps | ForEach-Object { [string]$_ })
    if ($localIps -contains $TestIp) { return $true }

    $extIp = Get-ExternalWanIp
    if (-not $extIp -or $TestIp -ne $extIp) { return $false }

    $activePorts = @([Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners() | ForEach-Object { $_.Port })
    foreach ($p in 443, 80, 30001) {
        if ($activePorts -contains $p) {
            try {
                $client = New-Object Net.Sockets.TcpClient
                $ar = $client.BeginConnect($TestIp, $p, $null, $null)
                $ok = $ar.AsyncWaitHandle.WaitOne(1500)
                $connected = $ok -and $client.Connected
                $client.Close()
                if ($connected) { return $true }
            } catch {}
        }
    }

    $listener = $null
    try {
        $listener = New-Object Net.Sockets.TcpListener([Net.IPAddress]::Any, 30001)
        $listener.Start()
        $client = New-Object Net.Sockets.TcpClient
        $ar = $client.BeginConnect($TestIp, 30001, $null, $null)
        $ok = $ar.AsyncWaitHandle.WaitOne(1500)
        $hit = $false
        if ($ok) {
            for ($w = 0; $w -lt 10; $w++) {
                if ($client.Connected -or $listener.Pending()) { $hit = $true; break }
                Start-Sleep -Milliseconds 20
            }
        }
        $client.Close()
        return [bool]$hit
    } catch {
        return $false
    } finally {
        if ($listener) { try { $listener.Stop() } catch {} }
    }
}

function Resolve-SmartMachineIp {
    $localIps = @(Get-LocalAdapterIps | ForEach-Object { [string]$_ })
    $extIp = Get-ExternalWanIp
    if ($extIp) {
        if ($localIps -contains $extIp) { return [string]$extIp }
        if (Test-IpReachableOnThisMachine $extIp) { return [string]$extIp }
    }
    if ($localIps.Count -gt 0 -and -not [string]::IsNullOrWhiteSpace($localIps[0])) {
        return [string]($localIps[0])
    }
    return '127.0.0.1'
}

function Ensure-ValidEnvForMachine {
    param([switch]$ForceRefreshIp)
    Repair-AllBomFiles
    $envFile = Join-Path $script:ProjectRoot '.env'
    $expectedProjectRoot = $script:ProjectRoot
    $expectedPatchRoot = Join-Path $script:ProjectRoot 'runtime\patchserver'
    $expectedNginxDir = Join-Path $script:ProjectRoot 'runtime\dependencies\nginx'
    $expectedMariaDir = Join-Path $script:ProjectRoot 'runtime\dependencies\mariadb'
    $guid = { [guid]::NewGuid().ToString('N') }

    if (-not (Test-Path $envFile)) {
        $smartIp = Resolve-SmartMachineIp
        $envText = @"
PROJECT_ROOT=$expectedProjectRoot
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=valiant2
MYSQL_PASSWORD=$(& $guid)
MYSQL_ACCOUNT_DATABASE=account
MYSQL_COMMON_DATABASE=common
MYSQL_LOG_DATABASE=log
MYSQL_PLAYER_DATABASE=player
SERVER_DB_HOST=127.0.0.1
SERVER_DB_PORT=30000
ADMINPAGE_IP=127.0.0.1
ADMINPAGE_PASSWORD=$(& $guid)
CLIENT_SERVER_NAME=VALIANT2
CLIENT_SERVER_IP=$smartIp
MARIADB_SERVICE=MariaDB
MARIADB_ROOT_PASSWORD=$(& $guid)
PANEL_DB_DATABASE=valiant_panel
PANEL_DB_USER=valiant_panel
PANEL_DB_PASSWORD=$(& $guid)
PANEL_P2P_CHANNEL_PORTS=30003,30005,30007,30009,30051
PUBLIC_IP=$smartIp
PANEL_BASE_URL=https://$smartIp/
PATCH_ROOT=$expectedPatchRoot
NGINX_DIR=$expectedNginxDir
MARIADB_DIR=$expectedMariaDir
"@
        Write-Utf8NoBom $envFile $envText
        Write-Host ".env otomatik olusturuldu (Algilanan IP: $smartIp)."
    }

    $s = Get-EnvSettings
    $changed = $false

    foreach ($pair in @(
        @{ Key = 'PROJECT_ROOT'; Val = $expectedProjectRoot },
        @{ Key = 'PATCH_ROOT';   Val = $expectedPatchRoot },
        @{ Key = 'NGINX_DIR';    Val = $expectedNginxDir },
        @{ Key = 'MARIADB_DIR';  Val = $expectedMariaDir }
    )) {
        if ($s[$pair.Key] -ne $pair.Val) {
            $s[$pair.Key] = $pair.Val
            $changed = $true
        }
    }

    $curIp = $s['PUBLIC_IP']
    if ($ForceRefreshIp -or (-not (Test-IpReachableOnThisMachine $curIp))) {
        $newIp = Resolve-SmartMachineIp
        if ($newIp -ne $curIp -or $s['CLIENT_SERVER_IP'] -ne $newIp) {
            Write-Host "IP adresi bu bilgisayar icin otomatik algilandi ve guncellendi: $curIp -> $newIp"
            $s['PUBLIC_IP'] = $newIp
            $s['CLIENT_SERVER_IP'] = $newIp
            $s['PANEL_BASE_URL'] = "https://$newIp/"
            $changed = $true
        }
    }

    if ($changed) {
        $lines = @()
        foreach ($k in $s.Keys) {
            $lines += "$k=$($s[$k])"
        }
        [IO.File]::WriteAllLines($envFile, $lines, $script:Utf8NoBom)
    }
    return $s
}

function Get-HardwareProfile {
    if ($script:CachedHwProfile) { return $script:CachedHwProfile }
    $threads = [Environment]::ProcessorCount
    if ($threads -lt 1) { $threads = 4 }
    $cores = [math]::Max(1, [int]($threads / 2))
    $cpuName = "Multi-Core Processor ($threads Threads)"
    $ramGb = 8.0
    try {
        $cpu = Get-CimInstance Win32_Processor -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($cpu) {
            $cpuName = $cpu.Name.Trim()
            if ($cpu.NumberOfCores) { $cores = [int]$cpu.NumberOfCores }
            if ($cpu.NumberOfLogicalProcessors) { $threads = [int]$cpu.NumberOfLogicalProcessors }
        }
        $cs = Get-CimInstance Win32_ComputerSystem -ErrorAction SilentlyContinue
        if ($cs -and $cs.TotalPhysicalMemory) {
            $ramGb = [math]::Round($cs.TotalPhysicalMemory / 1GB, 1)
        }
    } catch {}

    $innoMb = [math]::Min(16384, [math]::Max(512, [int]($ramGb * 1024 * 0.15)))
    $ariaMb = [math]::Min(2048, [math]::Max(128, [int]($ramGb * 1024 * 0.03)))

    $script:CachedHwProfile = [pscustomobject]@{
        CpuName             = $cpuName
        Cores               = $cores
        Threads             = $threads
        RamGb               = $ramGb
        MsBuildThreads      = $threads
        MariaDbBufferPoolMb = $innoMb
        MariaDbAriaBufferMb = $ariaMb
    }
    return $script:CachedHwProfile
}

function Optimize-HardwareConfig {
    $hw = Get-HardwareProfile
    $stampFile = Join-Path $script:ProjectRoot 'runtime\server\.state\hw_optimized.stamp'
    if (-not (Test-Path $stampFile)) {
        try {
            $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
            if ($isAdmin) {
                & powercfg.exe /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 2>$null | Out-Null
                Add-MpPreference -ExclusionPath $script:ProjectRoot -ErrorAction SilentlyContinue
                Add-MpPreference -ExclusionProcess 'MSBuild.exe','cl.exe','link.exe','FSArchiver.exe','game.exe','db.exe','mariadbd.exe' -ErrorAction SilentlyContinue
            }
            Write-Utf8NoBom $stampFile "$($hw.CpuName)|$($hw.Threads)|$($hw.RamGb)"
        } catch {}
    }

    $mariaDir = Get-MariaDbDir
    $myIni = Join-Path $mariaDir 'data\my.ini'
    if (Test-Path $myIni) {
        $dataDirSlash = (Join-Path $mariaDir 'data') -replace '\\','/'
        $pluginDirSlash = (Join-Path $mariaDir 'lib\plugin') -replace '\\','/'
        $newIni = @"
[mysqld]
datadir=$dataDirSlash
innodb_buffer_pool_size=$($hw.MariaDbBufferPoolMb)M
aria_pagecache_buffer_size=$($hw.MariaDbAriaBufferMb)M
key_buffer_size=256M
thread_pool_size=$($hw.Threads)
max_connections=1000
innodb_flush_log_at_trx_commit=2
join_buffer_size=4M
sort_buffer_size=4M
[client]
plugin-dir=$pluginDirSlash
"@
        $oldIni = Read-TextStripBom $myIni
        if ($oldIni -ne $newIni) {
            Write-Utf8NoBom $myIni $newIni
        }
    }

    $nginxConf = Join-Path (Get-NginxDir) 'conf\nginx.conf'
    if (Test-Path $nginxConf) {
        $nc = Read-TextStripBom $nginxConf
        $ncUpdated = $nc -replace '(?m)^worker_processes\s+\d+;', 'worker_processes  auto;'
        if ($ncUpdated -ne $nc) {
            Write-Utf8NoBom $nginxConf $ncUpdated
        }
    }
    return $hw
}

function Get-EnvSettings {
    $envFile = Join-Path $script:ProjectRoot '.env'
    $s = @{}
    if (Test-Path $envFile) {
        Remove-FileBomIfPresent $envFile | Out-Null
        $raw = Read-TextStripBom $envFile
        foreach ($row in ($raw -split "\r?\n")) {
            $line = $row.Trim().TrimStart([char]0xFEFF)
            if ($line -and !$line.StartsWith('#') -and $line.Contains('=')) {
                $k, $v = $line.Split('=', 2)
                $s[$k.Trim().TrimStart([char]0xFEFF)] = $v.Trim().Trim('"').Trim("'")
            }
        }
    }
    return $s
}

function Get-PublicBase {
    param($Settings)
    $ip = $Settings['PUBLIC_IP']; if (-not $ip) { $ip = $Settings['CLIENT_SERVER_IP'] }
    if (-not $ip) { $ip = '127.0.0.1' }
    return "https://$ip"
}

function Get-PatchRoot {
    param($Settings)
    return (Join-Path $script:ProjectRoot 'runtime\patchserver')
}

function Get-PhpExe {
    $cmd = Get-Command php.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $fastSearch = @(
        "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\PHP.PHP*",
        "$env:ProgramFiles\PHP*"
    )
    foreach ($pattern in $fastSearch) {
        $hit = Get-ChildItem $pattern -Recurse -Filter php.exe -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($hit) { return $hit.FullName }
    }
    $hit = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages","$env:ProgramFiles","${env:ProgramFiles(x86)}" -Recurse -Filter php.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($hit) { return $hit.FullName }
    throw 'php.exe bulunamadi (winget install PHP.PHP.8.3)'
}

function Get-PythonwExe {
    $cmd = Get-Command pythonw.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $hit = Get-ChildItem "$env:LOCALAPPDATA\Programs\Python","$env:ProgramFiles\Python*","${env:ProgramFiles(x86)}\Python*" -Recurse -Filter pythonw.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($hit) { return $hit.FullName }
    throw 'pythonw.exe bulunamadi (winget install Python.Python.3.12)'
}

function Get-MariaDbDir {
    return (Join-Path $script:ProjectRoot 'runtime\dependencies\mariadb')
}

function Get-MysqlClient {
    $projMaria = Join-Path (Get-MariaDbDir) 'bin'
    if (Test-Path $projMaria) {
        foreach ($name in 'mariadb.exe','mysql.exe') {
            $exe = Join-Path $projMaria $name
            if (Test-Path $exe) { return $exe }
        }
    }
    foreach ($name in 'mariadb.exe','mysql.exe') {
        $cmd = Get-Command $name -ErrorAction SilentlyContinue
        if ($cmd) { return $cmd.Source }
    }
    $hit = Get-ChildItem "$env:ProgramFiles\MariaDB*\bin" -Include 'mariadb.exe','mysql.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($hit) { return $hit.FullName }
    return $null
}

function Get-NginxDir {
    return (Join-Path $script:ProjectRoot 'runtime\dependencies\nginx')
}

function Get-NginxExe {
    $projNginx = Join-Path (Get-NginxDir) 'nginx.exe'
    if (Test-Path $projNginx) { return $projNginx }
    $cmd = Get-Command nginx.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    return $null
}

function Get-MsBuildExe {
    $vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
    if (Test-Path $vswhere) {
        $msb = & $vswhere -latest -products * -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' 2>$null | Select-Object -First 1
        if ($msb -and (Test-Path $msb)) { return $msb }
    }
    $cmd = Get-Command MSBuild.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    throw 'MSBuild.exe bulunamadi (Visual Studio 2022 Build Tools gerekli).'
}

function Get-CscExe {
    $fw64 = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
    if (Test-Path $fw64) { return $fw64 }
    $rtDir = [System.Runtime.InteropServices.RuntimeEnvironment]::GetRuntimeDirectory()
    $rtCsc = Join-Path $rtDir 'csc.exe'
    if (Test-Path $rtCsc) { return $rtCsc }
    throw 'csc.exe (.NET Framework 4) bulunamadi.'
}

function Ensure-PanelWritableDirs {
    $writable = Join-Path $script:ProjectRoot 'web\adminpanel\writable'
    foreach ($sub in 'cache','logs','session','uploads','debugbar') {
        $p = Join-Path $writable $sub
        if (-not (Test-Path $p)) {
            New-Item -ItemType Directory -Force -Path $p | Out-Null
        }
    }
}

function Ensure-PhpConfigured {
    $phpExe = $null
    try { $phpExe = Get-PhpExe } catch { return }
    if (-not $phpExe) { return }
    $phpDir = Split-Path $phpExe
    $phpIni = Join-Path $phpDir 'php.ini'
    if (-not (Test-Path $phpIni)) {
        $prod = Join-Path $phpDir 'php.ini-production'
        if (Test-Path $prod) { Copy-Item $prod $phpIni }
    }
    if (Test-Path $phpIni) {
        $content = Read-TextStripBom $phpIni
        $orig = $content
        $extDir = (Join-Path $phpDir 'ext') -replace '\\','/'
        $content = $content -replace ';\s*extension_dir\s*=\s*"ext"', "extension_dir = `"$extDir`""
        # Yorum orneklerindeki (;   extension=mysqli) yanlislikla acilmissa kapat
        $content = $content -replace '(?m)^extension=mysqli(\r?\n;\s*extension=/path/to/extension/mysqli\.so)', ';   extension=mysqli$1'
        foreach ($ext in 'curl','intl','mbstring','openssl','pdo_mysql','mysqli','gd','fileinfo') {
            $content = $content -replace "(?m)^;extension=$ext\b", "extension=$ext"
        }
        if ($content -ne $orig) {
            Write-Utf8NoBom $phpIni $content
        }
    }
}

function Ensure-NginxConfig {
    $nginxDir = Get-NginxDir
    $confDir = Join-Path $nginxDir 'conf'
    if (-not (Test-Path $confDir)) { return }
    $certDir = Join-Path $nginxDir 'certs'
    New-Item -ItemType Directory -Force -Path $certDir, (Join-Path $nginxDir 'html\.well-known\acme-challenge') | Out-Null
    $certF = (Join-Path $certDir 'cert.pem') -replace '\\','/'
    $keyF  = (Join-Path $certDir 'key.pem') -replace '\\','/'
    $nginxConf = @"
worker_processes  auto;

events {
    worker_connections  8192;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    server_tokens   off;

    limit_req_zone `$binary_remote_addr zone=panel:10m rate=50r/s;

    upstream panel_backend {
        server 127.0.0.1:8090;
        server 127.0.0.1:8092;
        server 127.0.0.1:8093;
        server 127.0.0.1:8094;
    }

    server {
        listen 80;
        server_name _;

        location ^~ /.well-known/acme-challenge/ {
            root html;
            default_type "text/plain";
        }

        location / {
            return 301 https://`$host`$request_uri;
        }
    }

    server {
        listen 443 ssl;
        server_name _;

        ssl_certificate     $certF;
        ssl_certificate_key $keyF;
        ssl_protocols       TLSv1.2 TLSv1.3;

        limit_req zone=panel burst=100 nodelay;

        location ^~ /.well-known/acme-challenge/ {
            root html;
            default_type "text/plain";
        }

        location /patcher/ {
            proxy_pass http://127.0.0.1:8091;
            proxy_set_header Host `$host;
            proxy_read_timeout 600s;
        }

        location /update/ {
            proxy_pass http://127.0.0.1:8091;
            proxy_set_header Host `$host;
            proxy_read_timeout 600s;
            proxy_buffering off;
        }

        location / {
            proxy_pass http://panel_backend;
            proxy_set_header Host `$host;
            proxy_set_header X-Real-IP `$remote_addr;
            proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
            proxy_read_timeout 60s;
        }
    }
}
"@
    $confPath = Join-Path $confDir 'nginx.conf'
    $oldConf = Read-TextStripBom $confPath
    if ($oldConf.Trim() -ne $nginxConf.Trim()) {
        Write-Utf8NoBom $confPath $nginxConf
    }
}

function Trust-CertificateOnWindows {
    param([string]$CertPemPath)
    if (-not (Test-Path $CertPemPath)) { return }
    try {
        $cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($CertPemPath)
        foreach ($loc in @([System.Security.Cryptography.X509Certificates.StoreLocation]::LocalMachine, [System.Security.Cryptography.X509Certificates.StoreLocation]::CurrentUser)) {
            try {
                $store = New-Object System.Security.Cryptography.X509Certificates.X509Store([System.Security.Cryptography.X509Certificates.StoreName]::Root, $loc)
                $store.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)
                $existing = $store.Certificates.Find([System.Security.Cryptography.X509Certificates.X509FindType]::FindByThumbprint, $cert.Thumbprint, $false)
                if ($existing.Count -eq 0) {
                    $store.Add($cert)
                }
                $store.Close()
                break
            } catch {}
        }
    } catch {}
}

function Reload-NginxIfRunning {
    $nginxExe = Get-NginxExe
    if (-not $nginxExe -or -not (Get-Process nginx -ErrorAction SilentlyContinue)) { return }
    $nginxDir = Get-NginxDir
    & $nginxExe -s reload -p $nginxDir 2>$null
    if ($LASTEXITCODE -ne 0) {
        try {
            Start-Process -FilePath $nginxExe -ArgumentList @('-s','reload','-p',$nginxDir) -Verb RunAs -WindowStyle Hidden -Wait -ErrorAction SilentlyContinue
        } catch {}
    }
}

function Stop-ServerProcesses {
    Get-Process -Name 'game','db' -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    if (Get-Process -Name 'game','db' -ErrorAction SilentlyContinue) {
        try {
            Start-Process -FilePath 'taskkill.exe' -ArgumentList '/F /IM game.exe /IM db.exe' -Verb RunAs -WindowStyle Hidden -Wait -ErrorAction SilentlyContinue
        } catch {}
    }
}

function Ensure-ValidSslCertificate {
    param($Settings, [switch]$ForceRenew)
    if (-not $Settings) { $Settings = Ensure-ValidEnvForMachine }
    $nginxDir = Get-NginxDir
    $certDir = Join-Path $nginxDir 'certs'
    New-Item -ItemType Directory -Force -Path $certDir | Out-Null
    $certPem = Join-Path $certDir 'cert.pem'
    $keyPem  = Join-Path $certDir 'key.pem'
    $cn = if ($Settings['PUBLIC_IP']) { $Settings['PUBLIC_IP'] } else { '127.0.0.1' }
    $isPublicIp = ($cn -match '^\d{1,3}(\.\d{1,3}){3}$') -and ($cn -notmatch '^(127\.|10\.|192\.168\.|169\.254\.|172\.(1[6-9]|2\d|3[01])\.)')

    $needsCert = $ForceRenew -or (-not (Test-Path $certPem)) -or (-not (Test-Path $keyPem))
    if (-not $needsCert) {
        try {
            $cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($certPem)
            if ($cert.NotAfter -lt (Get-Date).AddDays(2)) {
                $needsCert = $true
            } else {
                $sanMatch = ($cert.Subject -match [regex]::Escape($cn))
                foreach ($ext in $cert.Extensions) {
                    if ($ext.Oid.Value -eq '2.5.29.17') {
                        $sanText = $ext.Format($false)
                        if ($sanText -match [regex]::Escape($cn)) { $sanMatch = $true }
                    }
                }
                if (-not $sanMatch) {
                    $needsCert = $true
                } elseif ($isPublicIp -and ($cert.Issuer -eq $cert.Subject)) {
                    # Public IP icin self-signed kalmissa Let's Encrypt sertifikasina yukselt
                    $needsCert = $true
                }
            }
        } catch {
            $needsCert = $true
        }
    }

    if (-not $needsCert) {
        Ensure-NginxConfig
        return
    }

    $legoStore = Join-Path $certDir 'lego'
    $legoCert = Join-Path $legoStore "certificates\$cn.crt"
    $legoKey  = Join-Path $legoStore "certificates\$cn.key"

    # Eger lego icinde bu IP icin zaten gecerli sertifika varsa ve ForceRenew degilse dogrudan kopyala
    if (-not $ForceRenew -and (Test-Path $legoCert) -and (Test-Path $legoKey)) {
        try {
            $lc = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($legoCert)
            if ($lc.NotAfter -gt (Get-Date).AddDays(2)) {
                Copy-Item $legoCert $certPem -Force
                Copy-Item $legoKey  $keyPem  -Force
                Ensure-NginxConfig
                Reload-NginxIfRunning
                return
            }
        } catch {}
    }

    $obtainedLe = $false
    if ($isPublicIp) {
        $legoDir = Join-Path $script:ProjectRoot 'runtime\dependencies\lego'
        $legoExe = Join-Path $legoDir 'lego.exe'
        if (-not (Test-Path $legoExe)) {
            try {
                $legoVer = '5.3.1'
                $legoZip = Join-Path $env:TEMP 'lego.zip'
                $legoUrl = "https://github.com/go-acme/lego/releases/download/v${legoVer}/lego_v${legoVer}_windows_amd64.zip"
                Write-Host "lego indiriliyor ($legoVer)..."
                Invoke-WebRequest $legoUrl -OutFile $legoZip -UseBasicParsing
                New-Item -ItemType Directory -Force -Path $legoDir | Out-Null
                Expand-Archive $legoZip -DestinationPath $legoDir -Force
                Remove-Item $legoZip -ErrorAction SilentlyContinue
            } catch {}
        }
        if (Test-Path $legoExe) {
            Ensure-NginxConfig
            Reload-NginxIfRunning
            $listening80 = @([Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners() | ForEach-Object { $_.Port }) -contains 80
            Write-Host "Let's Encrypt IP sertifikasi aliniyor ($cn)..."
            $extraArgs = if ($ForceRenew -and (Test-Path $legoCert)) { @('--renew-force') } else { @() }
            if ($listening80) {
                # Once nginx html webroot, olmazsa panel webroot dene (nginx durdurmadan!)
                $htmlWebroot = Join-Path $nginxDir 'html'
                $panelWebroot = Join-Path $script:ProjectRoot 'web\adminpanel'
                & $legoExe run --email="admin@valiant2.com" --accept-tos --http --http.webroot="$htmlWebroot" --domains="$cn" --path="$legoStore" --profile="shortlived" @extraArgs
                if ($LASTEXITCODE -ne 0) {
                    & $legoExe run --email="admin@valiant2.com" --accept-tos --http --http.webroot="$panelWebroot" --domains="$cn" --path="$legoStore" --profile="shortlived" @extraArgs
                }
                Remove-Item (Join-Path $panelWebroot '.well-known') -Recurse -Force -ErrorAction SilentlyContinue
            } else {
                & $legoExe run --email="admin@valiant2.com" --accept-tos --http --http.address=":80" --domains="$cn" --path="$legoStore" --profile="shortlived" @extraArgs
            }
            if ($LASTEXITCODE -eq 0 -and (Test-Path $legoCert) -and (Test-Path $legoKey)) {
                Copy-Item $legoCert $certPem -Force
                Copy-Item $legoKey  $keyPem  -Force
                $obtainedLe = $true
                Write-Host "Let's Encrypt sertifikasi alindi ve aktif edildi ($cn)."
            }
        }
    }

    if (-not $obtainedLe) {
        Write-Host "Yerel/Self-signed SSL sertifikasi uretiliyor ($cn)..."
        $openssl = Get-ChildItem "$env:ProgramFiles\Git\usr\bin\openssl.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($openssl) {
            $sanEntries = @("DNS:localhost", "IP:127.0.0.1")
            if ($cn -match '^\d{1,3}(\.\d{1,3}){3}$') {
                if ($sanEntries -notcontains "IP:$cn") { $sanEntries = @("IP:$cn") + $sanEntries }
            } elseif ($cn -ne 'localhost') {
                $sanEntries = @("DNS:$cn") + $sanEntries
            }
            $sanConf = Join-Path $certDir 'san.cnf'
            $sanText = @"
[req]
default_bits=2048
prompt=no
default_md=sha256
distinguished_name=dn
x509_extensions=v3_req
[dn]
CN=$cn
[v3_req]
subjectAltName=$($sanEntries -join ',')
"@
            Write-Utf8NoBom $sanConf $sanText
            & $openssl.FullName req -x509 -newkey rsa:2048 -nodes -keyout $keyPem -out $certPem -days 3650 -config $sanConf 2>$null
            Remove-Item $sanConf -ErrorAction SilentlyContinue
            Trust-CertificateOnWindows $certPem
            Write-Host "Self-signed sertifika uretildi ve Windows guvenilir kok deposuna eklendi ($cn)."
        }
    }

    Ensure-NginxConfig
    Reload-NginxIfRunning
}
