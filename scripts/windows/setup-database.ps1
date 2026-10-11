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
$client = Get-ChildItem "$env:ProgramFiles\MariaDB*\bin\mariadb.exe","$env:ProgramFiles\MariaDB*\bin\mysql.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
if (!$client) { throw 'MariaDB command-line client was not found.' }
$service = Get-Service -Name $settings.MARIADB_SERVICE -ErrorAction Stop
if ($service.Status -ne 'Running') {
    Start-Service $service.Name
    $service.WaitForStatus('Running', [TimeSpan]::FromSeconds(30))
}
$previousPassword = $env:MYSQL_PWD
$env:MYSQL_PWD = $settings.MARIADB_ROOT_PASSWORD
try {
    $dump = Join-Path $root 'database\bootstrap.sql'
    Get-Content $dump -Raw | & $client.FullName --host=$($settings.MYSQL_HOST) --port=$($settings.MYSQL_PORT) --user=root
    if ($LASTEXITCODE -ne 0) { throw "Database import failed with code $LASTEXITCODE." }
    $sql = "CREATE USER IF NOT EXISTS '$($settings.MYSQL_USER)'@'localhost' IDENTIFIED BY '$($settings.MYSQL_PASSWORD)'; ALTER USER '$($settings.MYSQL_USER)'@'localhost' IDENTIFIED BY '$($settings.MYSQL_PASSWORD)'; GRANT ALL PRIVILEGES ON account.* TO '$($settings.MYSQL_USER)'@'localhost'; GRANT ALL PRIVILEGES ON common.* TO '$($settings.MYSQL_USER)'@'localhost'; GRANT ALL PRIVILEGES ON log.* TO '$($settings.MYSQL_USER)'@'localhost'; GRANT ALL PRIVILEGES ON player.* TO '$($settings.MYSQL_USER)'@'localhost'; FLUSH PRIVILEGES;"
    & $client.FullName --host=$($settings.MYSQL_HOST) --port=$($settings.MYSQL_PORT) --user=root --execute=$sql
    if ($LASTEXITCODE -ne 0) { throw "Database user setup failed with code $LASTEXITCODE." }
} finally {
    $env:MYSQL_PWD = $previousPassword
}
Write-Host 'Database initialized.'
