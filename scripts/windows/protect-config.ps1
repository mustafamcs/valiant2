$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$runtime = Join-Path $root 'runtime\server\main\srv1'
$dbConfig = Join-Path $runtime 'db\conf.txt'
$dbText = Get-Content $dbConfig -Raw
$dbText = $dbText -replace '(?m)^SQL_ACCOUNT\s*=.*$', 'SQL_ACCOUNT = "__FROM_ENV__"'
$dbText = $dbText -replace '(?m)^SQL_COMMON\s*=.*$', 'SQL_COMMON = "__FROM_ENV__"'
$dbText = $dbText -replace '(?m)^SQL_PLAYER\s*=.*$', 'SQL_PLAYER = "__FROM_ENV__"'
[IO.File]::WriteAllText($dbConfig, $dbText, [Text.UTF8Encoding]::new($false))
Get-ChildItem $runtime -Recurse -File -Filter CONFIG | ForEach-Object {
    $text = Get-Content $_.FullName -Raw
    $text = $text -replace '(?m)^(COMMON_SQL|LOG_SQL|PLAYER_SQL):.*$', '$1: __FROM_ENV__'
    $text = $text -replace '(?m)^ADMINPAGE_PASSWORD:.*$', 'ADMINPAGE_PASSWORD: __FROM_ENV__'
    [IO.File]::WriteAllText($_.FullName, $text, [Text.UTF8Encoding]::new($false))
}
$serverInfoFiles = @(
    (Join-Path $root 'assets\unpacked\data\root\serverinfo.py'),
    (Join-Path $root 'source\client\external\projects\CRootLib\Workplace\__cython\root_modules\serverinfo.py')
)
foreach ($f in $serverInfoFiles) {
    if (Test-Path $f) {
        $txt = [IO.File]::ReadAllText($f, [Text.Encoding]::UTF8)
        $txt = $txt -replace '(?m)^SERVER_NAME\s*=.*$', 'SERVER_NAME = "__FROM_ENV__"'
        $txt = $txt -replace '(?m)^SERVER_IP\s*=.*$', 'SERVER_IP = "__FROM_ENV__"'
        $txt = $txt -replace '(?m)^SERVER_IP_2\s*=.*$', 'SERVER_IP_2 = "127.0.0.1"'
        [IO.File]::WriteAllText($f, $txt, [Text.UTF8Encoding]::new($false))
    }
}
Write-Host 'Generated runtime credentials removed.'
