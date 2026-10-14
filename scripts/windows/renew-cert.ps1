$root = Split-Path (Split-Path $PSScriptRoot)
. (Join-Path $root 'scripts\windows\common.ps1')
$settings = Get-EnvSettings
$cn = $settings.PUBLIC_IP
$legoExe = Join-Path $root 'runtime\dependencies\lego\lego.exe'
$certDir = Join-Path (Get-NginxDir) 'certs'
$legoStore = Join-Path $certDir 'lego'
Get-Process nginx -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep 2
& $legoExe run --email='admin@valiant2.com' --accept-tos --http --http.address=':80' --domains=$cn --path=$legoStore --profile='shortlived' --renew-force
if ($LASTEXITCODE -eq 0) {
    Copy-Item (Join-Path $legoStore "certificates\$cn.crt") (Join-Path $certDir 'cert.pem') -Force
    Copy-Item (Join-Path $legoStore "certificates\$cn.key") (Join-Path $certDir 'key.pem') -Force
}
& (Join-Path $root 'scripts\windows\start-stack.ps1')
