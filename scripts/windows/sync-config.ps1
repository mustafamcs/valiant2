$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
. (Join-Path $PSScriptRoot 'common.ps1')
$settings = Ensure-ValidEnvForMachine
$required = @('MYSQL_HOST','MYSQL_PORT','MYSQL_USER','MYSQL_PASSWORD','MYSQL_ACCOUNT_DATABASE','MYSQL_COMMON_DATABASE','MYSQL_LOG_DATABASE','MYSQL_PLAYER_DATABASE','SERVER_DB_HOST','ADMINPAGE_IP','ADMINPAGE_PASSWORD','CLIENT_SERVER_NAME','CLIENT_SERVER_IP')
$missing = $required | Where-Object { !$settings.ContainsKey($_) -or [string]::IsNullOrWhiteSpace($settings[$_]) }
if ($missing) { throw "Missing .env values: $($missing -join ', ')" }
$runtime = Join-Path $root 'runtime\server\main\srv1'
$dbConfig = Join-Path $runtime 'db\conf.txt'
$origDbText = Get-Content $dbConfig -Raw
$dbText = $origDbText
$dbText = $dbText -replace '(?m)^SQL_ACCOUNT\s*=.*$', "SQL_ACCOUNT = `"$($settings.MYSQL_HOST) $($settings.MYSQL_ACCOUNT_DATABASE) $($settings.MYSQL_USER) $($settings.MYSQL_PASSWORD) $($settings.MYSQL_PORT)`""
$dbText = $dbText -replace '(?m)^SQL_COMMON\s*=.*$', "SQL_COMMON = `"$($settings.MYSQL_HOST) $($settings.MYSQL_COMMON_DATABASE) $($settings.MYSQL_USER) $($settings.MYSQL_PASSWORD) $($settings.MYSQL_PORT)`""
$dbText = $dbText -replace '(?m)^SQL_PLAYER\s*=.*$', "SQL_PLAYER = `"$($settings.MYSQL_HOST) $($settings.MYSQL_PLAYER_DATABASE) $($settings.MYSQL_USER) $($settings.MYSQL_PASSWORD) $($settings.MYSQL_PORT)`""
if ($dbText -ne $origDbText) {
    [IO.File]::WriteAllText($dbConfig, $dbText, [Text.UTF8Encoding]::new($false))
}
$coreDirs = Get-ServerCoreDirs
foreach ($dir in $coreDirs) {
    $cfgFile = Join-Path $dir 'CONFIG'
    if (-not (Test-Path $cfgFile -PathType Leaf)) { continue }
    $origText = Read-TextStripBom $cfgFile
    $text = $origText
    $dirName = Split-Path -Leaf $dir
    $playerDb = if ($dirName -eq 'auth') { $settings.MYSQL_ACCOUNT_DATABASE } else { $settings.MYSQL_PLAYER_DATABASE }
    $text = $text -replace '(?m)^DB_ADDR:.*$', "DB_ADDR: $($settings.SERVER_DB_HOST)"
    $text = $text -replace '(?m)^COMMON_SQL:.*$', "COMMON_SQL: $($settings.MYSQL_HOST) $($settings.MYSQL_USER) $($settings.MYSQL_PASSWORD) $($settings.MYSQL_COMMON_DATABASE) $($settings.MYSQL_PORT)"
    $text = $text -replace '(?m)^LOG_SQL:.*$', "LOG_SQL: $($settings.MYSQL_HOST) $($settings.MYSQL_USER) $($settings.MYSQL_PASSWORD) $($settings.MYSQL_LOG_DATABASE) $($settings.MYSQL_PORT)"
    $text = $text -replace '(?m)^PLAYER_SQL:.*$', "PLAYER_SQL: $($settings.MYSQL_HOST) $($settings.MYSQL_USER) $($settings.MYSQL_PASSWORD) $playerDb $($settings.MYSQL_PORT)"
    $text = $text -replace '(?m)^ADMINPAGE_IP1:.*$', "ADMINPAGE_IP1: $($settings.ADMINPAGE_IP)"
    $text = $text -replace '(?m)^ADMINPAGE_PASSWORD:.*$', "ADMINPAGE_PASSWORD: $($settings.ADMINPAGE_PASSWORD)"
    # BIND_IP: public IP - server announces this to clients for channel connect.
    # Must be the external IP so remote clients can reach the game core.
    $bindIp = $settings.PUBLIC_IP
    if (-not $bindIp) { $bindIp = $settings.CLIENT_SERVER_IP }
    if (-not $bindIp) { $bindIp = '127.0.0.1' }
    if ($text -match '(?m)^BIND_IP:') {
        $text = $text -replace '(?m)^BIND_IP:.*$', "BIND_IP: $bindIp"
    } else {
        $text = $text.TrimEnd() + "`nBIND_IP: $bindIp`n"
    }
    if ($text -ne $origText) {
        Write-Utf8NoBom $cfgFile $text
    }
}
$serverInfoFiles = @(
    (Join-Path $root 'assets\unpacked\data\root\serverinfo.py'),
    (Join-Path $root 'source\client\external\projects\CRootLib\Workplace\RootLib\serverinfo.py'),
    (Join-Path $root 'source\client\external\projects\CRootLib\Workplace\__cython\root_modules\serverinfo.py')
)
foreach ($file in $serverInfoFiles) {
    if (-not (Test-Path $file)) { continue }
    $origText = Read-TextStripBom $file
    $text = $origText
    $text = $text -replace '(?m)^SERVER_NAME\s*=.*$', "SERVER_NAME = `"$($settings.CLIENT_SERVER_NAME)`""
    $text = $text -replace '(?m)^SERVER_IP\s*=.*$', "SERVER_IP = `"$($settings.CLIENT_SERVER_IP)`""
    $text = $text -replace '(?m)^SERVER_IP_2\s*=.*$', 'SERVER_IP_2 = "127.0.0.1"'
    if ($text -ne $origText) {
        Write-Utf8NoBom $file $text
    }
}
# patchserver.json varsa base_url ve dizinleri guncelle
$patchRoot = Get-PatchRoot $settings
$patchCfg = Join-Path $patchRoot 'patchserver.json'
if (Test-Path $patchRoot) {
    $newPatchJson = @{
        game_dir    = (Join-Path $root 'runtime\client\game')
        patch_dir   = "$patchRoot\patch"
        patcher_dir = "$patchRoot\patcher"
        base_url    = (Get-PublicBase $settings)
    } | ConvertTo-Json
    $oldPatchJson = if (Test-Path $patchCfg) { Read-TextStripBom $patchCfg } else { '' }
    if ($oldPatchJson.Trim() -ne $newPatchJson.Trim()) {
        Write-Utf8NoBom $patchCfg $newPatchJson
    }
}
# --- Fix runtime symlink-reference files (Linux symlinks become plain text files on Windows git clone) ---
$shareConf = Join-Path $runtime 'share\conf'
$shareData = Join-Path $runtime 'share\data'
$shareLocale = Join-Path $runtime 'share\locale'

# locale/turkey -> locale/europe junction (LOCALE=turkey, dosyalar europe altinda)
$turkeyLocale = Join-Path $shareLocale 'turkey'
if (-not (Test-Path $turkeyLocale)) {
    $europeLocale = Join-Path $shareLocale 'europe'
    if (Test-Path $europeLocale) {
        New-Item -ItemType Junction -Path $turkeyLocale -Target $europeLocale -ErrorAction SilentlyContinue | Out-Null
    }
}

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

    # CRC, VERSION, item_names.txt, item_proto.txt, mob_names.txt, mob_proto.txt: copy from share/conf if reference
    foreach ($fname in @('CRC','VERSION','item_names.txt','item_proto.txt','mob_names.txt','mob_proto.txt')) {
        $f = Join-Path $dir $fname
        if ((Test-Path $f) -and -not (Test-Path $f -PathType Container)) {
            $c = (Get-Content $f -Raw -ErrorAction SilentlyContinue)
            if ($c -and $c.Trim() -match '^\.\./') {
                $src = Join-Path $shareConf $fname
                if (Test-Path $src) { Copy-Item $src $f -Force } else { Write-Utf8NoBom $f '' }
            }
        }
    }

    # cores: Linux core dump symlink text file -> remove on Windows
    $coresFile = Join-Path $dir 'cores'
    if ((Test-Path $coresFile) -and -not (Test-Path $coresFile -PathType Container)) {
        $c = (Get-Content $coresFile -Raw -ErrorAction SilentlyContinue)
        if ($c -and $c.Trim() -match '^\.\./') { Remove-Item $coresFile -Force -ErrorAction SilentlyContinue }
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

    # data, locale, mark: must be directory junctions (skip db dir - it has no data/locale)
    if ($dir -notmatch '\\db$') {
        $juncList = @(@{Name='data';Target=$shareData}, @{Name='locale';Target=$shareLocale})
        if ($dir -match '\\chan\\') {
            $chanMark = Join-Path $runtime 'chan\mark'
            if (Test-Path $chanMark) { $juncList += @{Name='mark';Target=$chanMark} }
        }
        foreach ($junc in $juncList) {
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

# Kok dizinde veya unpacked icinde olusabilecek gereksiz artik klasorleri temizle
Remove-Item (Join-Path $root '.lego'), (Join-Path $root 'logs'), (Join-Path $root 'assets\unpacked\logs') -Recurse -Force -ErrorAction SilentlyContinue

& (Join-Path $PSScriptRoot 'git-sanitize.ps1')
Write-Host 'Configuration synchronized from .env.'
