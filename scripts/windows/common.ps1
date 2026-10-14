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
    return ,$dirs
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
        (Join-Path $root 'source\client\external\projects\CRootLib\Workplace\RootLib\serverinfo.py'),
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
    return ,$ips
}

function Get-ExternalWanIp {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    foreach ($svc in 'https://api.ipify.org','https://ifconfig.me/ip','https://icanhazip.com') {
        try {
            $ip = (Invoke-WebRequest $svc -UseBasicParsing -TimeoutSec 3).Content.Trim()
            if ($ip -match '^\d{1,3}(\.\d{1,3}){3}$') { return $ip }
        } catch {}
    }
    return $null
}

function Test-IpReachableOnThisMachine {
    param([string]$TestIp)
    if ([string]::IsNullOrWhiteSpace($TestIp)) { return $false }
    if ($TestIp -eq '127.0.0.1') { return $true }
    $localIps = @(Get-LocalAdapterIps)
    if ($localIps -contains $TestIp) { return $true }

    $extIp = Get-ExternalWanIp
    if (-not $extIp -or $TestIp -ne $extIp) { return $false }

    $activePorts = @([Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners() | ForEach-Object { $_.Port })
    foreach ($p in 443, 80, 30001) {
        if ($activePorts -contains $p) {
            try {
                $client = New-Object Net.Sockets.TcpClient
                $ar = $client.BeginConnect($TestIp, $p, $null, $null)
                $ok = $ar.AsyncWaitHandle.WaitOne(500)
                $client.Close()
                if ($ok) { return $true }
            } catch {}
        }
    }

    $listener = $null
    try {
        $listener = New-Object Net.Sockets.TcpListener([Net.IPAddress]::Any, 30001)
        $listener.Start()
        $client = New-Object Net.Sockets.TcpClient
        $ar = $client.BeginConnect($TestIp, 30001, $null, $null)
        $ok = $ar.AsyncWaitHandle.WaitOne(500)
        $hit = $ok -and $listener.Pending()
        $client.Close()
        return [bool]$hit
    } catch {
        return $false
    } finally {
        if ($listener) { try { $listener.Stop() } catch {} }
    }
}

function Resolve-SmartMachineIp {
    $localIps = @(Get-LocalAdapterIps)
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
    $expectedPatchRoot = Join-Path $script:ProjectRoot 'runtime\patchserver'
    $guid = { [guid]::NewGuid().ToString('N') }

    if (-not (Test-Path $envFile)) {
        $smartIp = Resolve-SmartMachineIp
        $envText = @"
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
"@
        Write-Utf8NoBom $envFile $envText
        Write-Host ".env otomatik olusturuldu (Algilanan IP: $smartIp)."
    }

    $s = Get-EnvSettings
    $changed = $false

    if ($s['PATCH_ROOT'] -ne $expectedPatchRoot) {
        $s['PATCH_ROOT'] = $expectedPatchRoot
        $changed = $true
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
