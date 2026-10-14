$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$settings = @{}
Get-Content (Join-Path $root '.env') | ForEach-Object {
    $line = $_.Trim()
    if ($line -and !$line.StartsWith('#') -and $line.Contains('=')) {
        $key, $value = $line.Split('=', 2)
        $settings[$key.Trim()] = $value.Trim().Trim('"').Trim("'")
    }
}
. (Join-Path $PSScriptRoot 'common.ps1')
$clientPath = Get-MysqlClient
if (!$clientPath) { throw 'MariaDB command-line client was not found.' }
$client = Get-Item $clientPath
$service = Get-Service -Name $settings.MARIADB_SERVICE -ErrorAction Stop
if ($service.Status -ne 'Running') {
    Start-Service $service.Name
    $service.WaitForStatus('Running', [TimeSpan]::FromSeconds(30))
}
$previousPassword = $env:MYSQL_PWD
$env:MYSQL_PWD = $settings.MARIADB_ROOT_PASSWORD
try {
    # --force: allow re-run when tables already exist
    # --default-character-set=binary: bootstrap.sql contains mixed encodings
    #   (utf8mb4 for most tables, latin5 for proto data - SET NAMES markers handle switching)
    $charsetArg = '--default-character-set=binary'
    $dump = Join-Path $root 'database\bootstrap.sql'
    # Use cmd /c with input redirection to avoid PowerShell encoding mangling
    & cmd.exe /c "`"$($client.FullName)`" --host=$($settings.MYSQL_HOST) --port=$($settings.MYSQL_PORT) --user=root --force $charsetArg < `"$dump`" 2>nul"
    if ($LASTEXITCODE -ne 0) { throw "Database import failed with code $LASTEXITCODE." }
    $extra = Join-Path $root 'database\extra_tables.sql'
    if (Test-Path $extra) {
        & cmd.exe /c "`"$($client.FullName)`" --host=$($settings.MYSQL_HOST) --port=$($settings.MYSQL_PORT) --user=root --force --default-character-set=utf8mb4 player < `"$extra`" 2>nul"
        if ($LASTEXITCODE -ne 0) { throw "Extra tables import failed with code $LASTEXITCODE." }
    }
    $dropSeed = Join-Path $root 'database\drop_seed.sql'
    if (Test-Path $dropSeed) {
        & cmd.exe /c "`"$($client.FullName)`" --host=$($settings.MYSQL_HOST) --port=$($settings.MYSQL_PORT) --user=root --force --default-character-set=utf8mb4 player < `"$dropSeed`" 2>nul"
        if ($LASTEXITCODE -ne 0) { throw "Drop seed import failed with code $LASTEXITCODE." }
    }
    $sql = "CREATE USER IF NOT EXISTS '$($settings.MYSQL_USER)'@'localhost' IDENTIFIED BY '$($settings.MYSQL_PASSWORD)'; ALTER USER '$($settings.MYSQL_USER)'@'localhost' IDENTIFIED BY '$($settings.MYSQL_PASSWORD)'; GRANT ALL PRIVILEGES ON account.* TO '$($settings.MYSQL_USER)'@'localhost'; GRANT ALL PRIVILEGES ON common.* TO '$($settings.MYSQL_USER)'@'localhost'; GRANT ALL PRIVILEGES ON log.* TO '$($settings.MYSQL_USER)'@'localhost'; GRANT ALL PRIVILEGES ON player.* TO '$($settings.MYSQL_USER)'@'localhost'; FLUSH PRIVILEGES;"
    & cmd.exe /c "`"$($client.FullName)`" --host=$($settings.MYSQL_HOST) --port=$($settings.MYSQL_PORT) --user=root --execute=`"$sql`" 2>nul"
    if ($LASTEXITCODE -ne 0) { throw "Database user setup failed with code $LASTEXITCODE." }

    # Panel veritabani + kullanicisi (web\adminpanel\sql.sql)
    $pdb = $settings.PANEL_DB_DATABASE; if (-not $pdb) { $pdb = 'valiant_panel' }
    $puser = $settings.PANEL_DB_USER; if (-not $puser) { $puser = 'valiant_panel' }
    $ppass = $settings.PANEL_DB_PASSWORD
    $sql = "CREATE DATABASE IF NOT EXISTS ``$pdb`` CHARACTER SET utf8mb4; CREATE USER IF NOT EXISTS '$puser'@'localhost' IDENTIFIED BY '$ppass'; ALTER USER '$puser'@'localhost' IDENTIFIED BY '$ppass'; GRANT ALL PRIVILEGES ON ``$pdb``.* TO '$puser'@'localhost'; FLUSH PRIVILEGES;"
    & cmd.exe /c "`"$($client.FullName)`" --host=$($settings.MYSQL_HOST) --port=$($settings.MYSQL_PORT) --user=root --execute=`"$sql`" 2>nul"
    if ($LASTEXITCODE -ne 0) { throw "Panel database setup failed with code $LASTEXITCODE." }
    $panelSql = Join-Path $root 'web\adminpanel\sql.sql'
    if (Test-Path $panelSql) {
        & cmd.exe /c "`"$($client.FullName)`" --host=$($settings.MYSQL_HOST) --port=$($settings.MYSQL_PORT) --user=root --force --default-character-set=utf8mb4 $pdb < `"$panelSql`" 2>nul"
        # --force: tables already exist is not fatal on re-run
    }
} finally {
    $env:MYSQL_PWD = $previousPassword
}
Write-Host 'Database initialized.'
