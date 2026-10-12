# Oyun hesabi olusturur ve karaktere IMPLEMENTOR (GM) yetkisi verir.
# Kullanim: create-account.cmd  (interaktif) — hesap yoksa olusturur, varsa sifre/yetki gunceller.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$settings = Get-EnvSettings

$mysqlCli = Get-MysqlClient
if (-not $mysqlCli) { throw 'MariaDB client bulunamadi.' }
$mysqlCli = Get-Item $mysqlCli

$adminLogin = Read-Host 'Oyun giris ID (account login)'
if (-not $adminLogin) { Write-Host 'Iptal.'; exit 0 }
$adminPass = Read-Host 'Sifre'
$gmName    = Read-Host 'GM/IMPLEMENTOR yetkisi verilecek karakter adi (bos birakilabilir)'

$prev = $env:MYSQL_PWD; $env:MYSQL_PWD = $settings['MARIADB_ROOT_PASSWORD']
try {
    $sql = "INSERT INTO account.account (login,password,social_id,email,status) VALUES ('$adminLogin',PASSWORD('$adminPass'),'1234567','admin@local','OK') ON DUPLICATE KEY UPDATE password=PASSWORD('$adminPass'), status='OK';"
    if ($gmName) {
        $sql += "INSERT INTO common.gmlist (mAccount,mName,mContactIP,mServerIP,mAuthority) VALUES ('$adminLogin','$gmName','ALL','ALL','IMPLEMENTOR') ON DUPLICATE KEY UPDATE mAuthority='IMPLEMENTOR';"
    }
    & $mysqlCli.FullName --host=$($settings.MYSQL_HOST) --port=$($settings.MYSQL_PORT) --user=root --execute=$sql
    if ($LASTEXITCODE -ne 0) { throw "SQL hatasi: $LASTEXITCODE" }
    Write-Host "Tamam: hesap '$adminLogin' hazir$(if ($gmName) {", '$gmName' = IMPLEMENTOR"})."
} finally { $env:MYSQL_PWD = $prev }
