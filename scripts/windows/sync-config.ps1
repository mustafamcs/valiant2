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
    [IO.File]::WriteAllText($_.FullName, $text, [Text.UTF8Encoding]::new($false))
}
$serverInfoFiles = @(
    (Join-Path $root 'assets\unpacked\data\root\serverinfo.py'),
    (Join-Path $root 'source\client\external\projects\CRootLib\Workplace\__cython\root_modules\serverinfo.py')
)
foreach ($file in $serverInfoFiles) {
    $text = Get-Content $file -Raw
    $text = $text -replace '(?m)^SERVER_NAME\s*=.*$', "SERVER_NAME = `"$($settings.CLIENT_SERVER_NAME)`""
    $text = $text -replace '(?m)^SERVER_IP\s*=.*$', "SERVER_IP = `"$($settings.CLIENT_SERVER_IP)`""
    $text = $text -replace '(?m)^SERVER_IP_2\s*=.*$', "SERVER_IP_2 = `"$($settings.CLIENT_SERVER_IP)`""
    [IO.File]::WriteAllText($file, $text, [Text.UTF8Encoding]::new($false))
}
Write-Host 'Configuration synchronized from .env.'
