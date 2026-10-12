$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$envFile = Join-Path $root '.env'
$settings = @{}
Get-Content $envFile | ForEach-Object {
    $line = $_.Trim()
    if ($line -and !$line.StartsWith('#') -and $line.Contains('=')) {
        $key, $value = $line.Split('=', 2)
        $settings[$key.Trim()] = $value.Trim().Trim('"').Trim("'")
    }
}
$required = @('MYSQL_HOST','MYSQL_PORT','MYSQL_USER','MYSQL_PASSWORD','MYSQL_ACCOUNT_DATABASE','MYSQL_COMMON_DATABASE','MYSQL_LOG_DATABASE','MYSQL_PLAYER_DATABASE','SERVER_DB_HOST','ADMINPAGE_IP','ADMINPAGE_PASSWORD','CLIENT_SERVER_NAME','CLIENT_SERVER_IP')
$missing = $required | Where-Object { !$settings.ContainsKey($_) -or [string]::IsNullOrWhiteSpace($settings[$_]) }
if ($missing) { throw "Missing .env values: $($missing -join ', ')" }
$runtime = Join-Path $root 'runtime\server\main\srv1'
$dbConfig = Join-Path $runtime 'db\conf.txt'
$dbText = Get-Content $dbConfig -Raw
$dbText = $dbText -replace '(?m)^SQL_ACCOUNT\s*=.*$', "SQL_ACCOUNT = `"$($settings.MYSQL_HOST) $($settings.MYSQL_ACCOUNT_DATABASE) $($settings.MYSQL_USER) $($settings.MYSQL_PASSWORD) $($settings.MYSQL_PORT)`""
$dbText = $dbText -replace '(?m)^SQL_COMMON\s*=.*$', "SQL_COMMON = `"$($settings.MYSQL_HOST) $($settings.MYSQL_COMMON_DATABASE) $($settings.MYSQL_USER) $($settings.MYSQL_PASSWORD) $($settings.MYSQL_PORT)`""
$dbText = $dbText -replace '(?m)^SQL_PLAYER\s*=.*$', "SQL_PLAYER = `"$($settings.MYSQL_HOST) $($settings.MYSQL_PLAYER_DATABASE) $($settings.MYSQL_USER) $($settings.MYSQL_PASSWORD) $($settings.MYSQL_PORT)`""
[IO.File]::WriteAllText($dbConfig, $dbText, [Text.UTF8Encoding]::new($false))
Get-ChildItem $runtime -Recurse -File -Filter CONFIG | ForEach-Object {
    $text = Get-Content $_.FullName -Raw
    $playerDb = if ($_.Directory.Name -eq 'auth') { $settings.MYSQL_ACCOUNT_DATABASE } else { $settings.MYSQL_PLAYER_DATABASE }
    $text = $text -replace '(?m)^DB_ADDR:.*$', "DB_ADDR: $($settings.SERVER_DB_HOST)"
    $text = $text -replace '(?m)^COMMON_SQL:.*$', "COMMON_SQL: $($settings.MYSQL_HOST) $($settings.MYSQL_USER) $($settings.MYSQL_PASSWORD) $($settings.MYSQL_COMMON_DATABASE) $($settings.MYSQL_PORT)"
    $text = $text -replace '(?m)^LOG_SQL:.*$', "LOG_SQL: $($settings.MYSQL_HOST) $($settings.MYSQL_USER) $($settings.MYSQL_PASSWORD) $($settings.MYSQL_LOG_DATABASE) $($settings.MYSQL_PORT)"
    $text = $text -replace '(?m)^PLAYER_SQL:.*$', "PLAYER_SQL: $($settings.MYSQL_HOST) $($settings.MYSQL_USER) $($settings.MYSQL_PASSWORD) $playerDb $($settings.MYSQL_PORT)"
    $text = $text -replace '(?m)^ADMINPAGE_IP1:.*$', "ADMINPAGE_IP1: $($settings.ADMINPAGE_IP)"
    $text = $text -replace '(?m)^ADMINPAGE_PASSWORD:.*$', "ADMINPAGE_PASSWORD: $($settings.ADMINPAGE_PASSWORD)"
    # BIND_IP: internal IP (adapter IP for socket bind; public IP is announced via serverinfo.py)
    # game.exe treats "0" prefix as "no IP" and exits, so we cannot use 0.0.0.0
    $bindIp = $null
    try {
        $bindIp = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -ne '127.0.0.1' -and $_.PrefixOrigin -ne 'WellKnown' } | Select-Object -First 1).IPAddress
    } catch {}
    if (-not $bindIp) { $bindIp = '127.0.0.1' }
    if ($text -match '(?m)^BIND_IP:') {
        $text = $text -replace '(?m)^BIND_IP:.*$', "BIND_IP: $bindIp"
    } else {
        $text = $text.TrimEnd() + "`nBIND_IP: $bindIp`n"
    }
    [IO.File]::WriteAllText($_.FullName, $text, [Text.UTF8Encoding]::new($false))
}
$serverInfoFiles = @(
    (Join-Path $root 'assets\unpacked\data\root\serverinfo.py'),
    (Join-Path $root 'source\client\external\projects\CRootLib\Workplace\RootLib\serverinfo.py')
)
foreach ($file in $serverInfoFiles) {
    if (-not (Test-Path $file)) { continue }
    $text = Get-Content $file -Raw
    $text = $text -replace '(?m)^SERVER_NAME\s*=.*$', "SERVER_NAME = `"$($settings.CLIENT_SERVER_NAME)`""
    $text = $text -replace '(?m)^SERVER_IP\s*=.*$', "SERVER_IP = `"$($settings.CLIENT_SERVER_IP)`""
    $text = $text -replace '(?m)^SERVER_IP_2\s*=.*$', "SERVER_IP_2 = `"$($settings.CLIENT_SERVER_IP)`""
    [IO.File]::WriteAllText($file, $text, [Text.UTF8Encoding]::new($false))
}
# --- Fix runtime symlink-reference files (Linux symlinks become plain text files on Windows git clone) ---
$shareConf = Join-Path $runtime 'share\conf'
$shareData = Join-Path $runtime 'share\data'
$shareLocale = Join-Path $runtime 'share\locale'

$coreDirs = @(
    (Join-Path $runtime 'auth'),
    (Join-Path $runtime 'db')
) + @(Get-ChildItem (Join-Path $runtime 'chan') -Recurse -Directory | Where-Object { $_.Name -match '^core' } | ForEach-Object { $_.FullName })

foreach ($dir in $coreDirs) {
    if (-not (Test-Path $dir)) { continue }

    # CMD: if file content looks like a relative path reference, empty it
    $cmdFile = Join-Path $dir 'CMD'
    if ((Test-Path $cmdFile) -and -not (Test-Path $cmdFile -PathType Container)) {
        $c = (Get-Content $cmdFile -Raw -ErrorAction SilentlyContinue)
        if ($c -and $c.Trim() -match '^\.\./') { [IO.File]::WriteAllText($cmdFile, '', [Text.UTF8Encoding]::new($false)) }
    }

    # CRC, VERSION: copy from share/conf if reference
    foreach ($fname in @('CRC','VERSION')) {
        $f = Join-Path $dir $fname
        if ((Test-Path $f) -and -not (Test-Path $f -PathType Container)) {
            $c = (Get-Content $f -Raw -ErrorAction SilentlyContinue)
            if ($c -and $c.Trim() -match '^\.\./') {
                $src = Join-Path $shareConf $fname
                if (Test-Path $src) { Copy-Item $src $f -Force } else { [IO.File]::WriteAllText($f, '', [Text.UTF8Encoding]::new($false)) }
            }
        }
    }

    # PTS, state_user_count, srv1-*: empty if reference
    foreach ($fname in @('PTS','state_user_count')) {
        $f = Join-Path $dir $fname
        if ((Test-Path $f) -and -not (Test-Path $f -PathType Container)) {
            $c = (Get-Content $f -Raw -ErrorAction SilentlyContinue)
            if ($c -and $c.Trim() -match '^\.\./') { [IO.File]::WriteAllText($f, '', [Text.UTF8Encoding]::new($false)) }
        }
    }
    Get-ChildItem $dir -File -Filter 'srv1-*' -ErrorAction SilentlyContinue | ForEach-Object {
        $c = (Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue)
        if ($c -and $c.Trim() -match '^\.\./') { [IO.File]::WriteAllText($_.FullName, '', [Text.UTF8Encoding]::new($false)) }
    }

    # BANIP: empty if contains a path reference
    $banipFile = Join-Path $dir 'BANIP'
    if ((Test-Path $banipFile) -and -not (Test-Path $banipFile -PathType Container)) {
        $c = (Get-Content $banipFile -Raw -ErrorAction SilentlyContinue)
        if ($c -and $c.Trim() -match '^\.\./') { [IO.File]::WriteAllText($banipFile, '', [Text.UTF8Encoding]::new($false)) }
    } elseif (-not (Test-Path $banipFile)) {
        [IO.File]::WriteAllText($banipFile, '', [Text.UTF8Encoding]::new($false))
    }

    # log: must be a directory (not a reference file)
    $logPath = Join-Path $dir 'log'
    if ((Test-Path $logPath) -and -not (Test-Path $logPath -PathType Container)) {
        Remove-Item $logPath -Force
        New-Item -ItemType Directory -Path $logPath -Force | Out-Null
    } elseif (-not (Test-Path $logPath)) {
        New-Item -ItemType Directory -Path $logPath -Force | Out-Null
    }

    # data, locale: must be directory junctions (skip db dir — it has no data/locale)
    if ($dir -notmatch '\\db$') {
        foreach ($junc in @(@{Name='data';Target=$shareData}, @{Name='locale';Target=$shareLocale})) {
            $jp = Join-Path $dir $junc.Name
            if ((Test-Path $jp) -and -not (Test-Path $jp -PathType Container)) {
                Remove-Item $jp -Force
            }
            if (-not (Test-Path $jp)) {
                New-Item -ItemType Junction -Path $jp -Target $junc.Target -ErrorAction SilentlyContinue | Out-Null
            }
        }
    }
}

& (Join-Path $PSScriptRoot 'git-sanitize.ps1')
Write-Host 'Configuration synchronized from .env.'
