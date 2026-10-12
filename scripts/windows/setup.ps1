# VALIANT2 sifirdan kurulum — yeni makinede tek komut.
# Yapar: winget bagimliliklari, .env uretimi, MariaDB, LFS, DB sema, derleme,
# nginx kurulumu + sertifika, patchserver dagitimi, zamanlanmis gorevler, firewall.
$ErrorActionPreference = 'Stop'
$principal = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
if (!$principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell.exe -Verb RunAs -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$PSCommandPath`"") -Wait
    exit $LASTEXITCODE
}
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
. (Join-Path $PSScriptRoot 'common.ps1')

function Install-Package([string]$id, [string[]]$extra = @()) {
    & winget list --id $id --exact --accept-source-agreements | Out-Null
    if ($LASTEXITCODE -eq 0) { Write-Host "$id zaten kurulu."; return }
    Write-Host "$id kuruluyor..."
    & winget install --id $id --exact --accept-package-agreements --accept-source-agreements --silent @extra
    if ($LASTEXITCODE -ne 0) { throw "$id installation failed with code $LASTEXITCODE." }
}
if (!(Get-Command winget -ErrorAction SilentlyContinue)) { throw 'Windows Package Manager (winget) is required.' }

# --- 1) Bagimliliklar ---
Install-Package 'Git.Git'
Install-Package 'GitHub.GitLFS'
Install-Package 'Microsoft.VCRedist.2015+.x86'
Install-Package 'Microsoft.DotNet.Framework.DeveloperPack_4'
Install-Package 'Microsoft.VisualStudio.2022.BuildTools' @('--override','--wait --passive --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended')
Install-Package 'PHP.PHP.8.3'
Install-Package 'Python.Python.3.12'

# --- 2) .env ---
$envFile = Join-Path $root '.env'
if (!(Test-Path $envFile)) {
    $dbPassword = ([guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N'))
    $adminPassword = [guid]::NewGuid().ToString('N')
    $rootPassword = ([guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N'))
    $panelDbPass = [guid]::NewGuid().ToString('N')
    $content = Get-Content (Join-Path $root '.env.example') -Raw
    $content = $content -replace '(?m)^MYSQL_PASSWORD=.*$', "MYSQL_PASSWORD=$dbPassword"
    $content = $content -replace '(?m)^ADMINPAGE_PASSWORD=.*$', "ADMINPAGE_PASSWORD=$adminPassword"
    $content = $content -replace '(?m)^MARIADB_ROOT_PASSWORD=.*$', "MARIADB_ROOT_PASSWORD=$rootPassword"
    $content = $content -replace '(?m)^PANEL_DB_PASSWORD=.*$', "PANEL_DB_PASSWORD=$panelDbPass"
    [IO.File]::WriteAllText($envFile, $content, [Text.UTF8Encoding]::new($false))
    Write-Host ".env uretildi (rastgele sifrelerle)."
}
$settings = Get-EnvSettings
if (-not $settings.PUBLIC_IP -or $settings.PUBLIC_IP -eq '127.0.0.1') {
    Write-Host 'NOT: .env icindeki PUBLIC_IP su an 127.0.0.1 — disaridan erisim icin gercek IP/domain yazip sync-config calistirin.'
}

# --- 3) MariaDB ---
$rootPassword = $settings['MARIADB_ROOT_PASSWORD']
Install-Package 'MariaDB.Server' @('--override',"SERVICENAME=MariaDB PASSWORD=$rootPassword /qn")

# --- 4) Git LFS ---
$git = Get-Command git.exe -ErrorAction SilentlyContinue
if (!$git) { $env:Path = "$env:ProgramFiles\Git\cmd;$env:Path"; $git = Get-Command git.exe -ErrorAction Stop }
& $git.Source lfs install --local
& $git.Source lfs pull
if ($LASTEXITCODE -ne 0) { throw "Git LFS download failed with code $LASTEXITCODE." }

# --- 5) Nginx ---
if (-not (Get-NginxExe)) {
    Write-Host 'nginx indiriliyor...'
    $zip = Join-Path $env:TEMP 'nginx.zip'
    Invoke-WebRequest 'https://nginx.org/download/nginx-1.27.5.zip' -OutFile $zip -UseBasicParsing
    Expand-Archive $zip 'C:\' -Force
    Remove-Item $zip
}
$nginxDir = Split-Path (Get-NginxExe)
# Sertifika (yoksa Git'in openssl'i ile self-signed uret — PUBLIC_IP icin)
$certDir = Join-Path $root 'deploy\certs'
New-Item -ItemType Directory -Force -Path $certDir | Out-Null
$certPem = Join-Path $certDir 'cert.pem'; $keyPem = Join-Path $certDir 'key.pem'
if (-not (Test-Path $certPem)) {
    $openssl = Get-ChildItem "$env:ProgramFiles\Git\usr\bin\openssl.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $openssl) { throw 'openssl bulunamadi (Git kurulumuyla gelmeli)' }
    $cn = if ($settings.PUBLIC_IP) { $settings.PUBLIC_IP } else { 'localhost' }
    & $openssl.FullName req -x509 -newkey rsa:2048 -nodes -keyout $keyPem -out $certPem -days 3650 -subj "/CN=$cn"
    Write-Host "Self-signed sertifika uretildi ($cn). Public IP ile Let's Encrypt icin lego kullanilabilir."
}
# nginx.conf'i sablon + sertifika yollariyla yaz
$tpl = Get-Content (Join-Path $root 'deploy\nginx.conf.template') -Raw
$tpl = $tpl -replace '__CERT_PEM__', ($certPem -replace '\\','/') -replace '__KEY_PEM__', ($keyPem -replace '\\','/')
[IO.File]::WriteAllText((Join-Path $nginxDir 'conf\nginx.conf'), $tpl, [Text.UTF8Encoding]::new($false))
& (Join-Path $nginxDir 'nginx.exe') -t -p $nginxDir
if ($LASTEXITCODE -ne 0) { throw 'nginx.conf testi basarisiz.' }

# --- 6) Patchserver dagitimi ---
$patchRoot = Get-PatchRoot $settings
New-Item -ItemType Directory -Force -Path "$patchRoot\patch\files", "$patchRoot\patcher" | Out-Null
Copy-Item (Join-Path $root 'patchserver\*') $patchRoot -Recurse -Force
@{
    game_dir    = (Join-Path $root 'runtime\client\game')
    patch_dir   = "$patchRoot\patch"
    patcher_dir = "$patchRoot\patcher"
    base_url    = (Get-PublicBase $settings)
} | ConvertTo-Json | Set-Content (Join-Path $patchRoot 'patchserver.json') -Encoding ascii
Write-Host "Patchserver kuruldu: $patchRoot"

# --- 7) Zamanlanmis gorevler (oturum acilisinda stack'i calistir) ---
$cmd = Join-Path $PSScriptRoot 'start-stack.cmd'
$act = New-ScheduledTaskAction -Execute $cmd -WorkingDirectory $PSScriptRoot
$trg = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName 'VALIANT2-Stack' -Action $act -Trigger $trg -Force -Description 'VALIANT2 web/patch altyapisi' | Out-Null

# --- 8) Firewall (oyun + web portlari; varsa atla) ---
$ports = 80,443,30001,30003,30005,30007,30009,30051
if (-not (Get-NetFirewallRule -DisplayName 'VALIANT2-Public' -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -DisplayName 'VALIANT2-Public' -Direction Inbound -Action Allow -Protocol TCP -LocalPort $ports | Out-Null
}

# --- 9) DB + derleme ---
& (Join-Path $PSScriptRoot 'setup-database.ps1')
& (Join-Path $PSScriptRoot 'build-all.ps1')
& (Join-Path $PSScriptRoot 'build-patcher.ps1')

Write-Host ''
Write-Host 'VALIANT2 setup completed.'
Write-Host "Web altyapisi: $PSScriptRoot\start-stack.cmd   Oyun: $PSScriptRoot\start-server.cmd"
Write-Host "Durum kontrolu: $PSScriptRoot\stack-status.cmd"
