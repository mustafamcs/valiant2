$root = Split-Path (Split-Path $PSScriptRoot)
. (Join-Path $root 'scripts\windows\common.ps1')
$settings = Ensure-ValidEnvForMachine
Ensure-ValidSslCertificate $settings -ForceRenew
& (Join-Path $root 'scripts\windows\start-stack.ps1')
