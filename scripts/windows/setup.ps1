# VALIANT2 sifirdan kurulum - yeni makinede tek komut.
# Yapar: winget bagimliliklari, .env uretimi, MariaDB, LFS, DB sema, derleme,
# nginx kurulumu + sertifika, patchserver dagitimi, zamanlanmis gorevler, firewall.
param([switch]$NonInteractive)
$ErrorActionPreference = 'Stop'
$principal = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
if (!$principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell.exe -Verb RunAs -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$PSCommandPath`"") -Wait
    exit $LASTEXITCODE
}
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
. (Join-Path $PSScriptRoot 'common.ps1')

function Install-Package([string]$id, [string[]]$extra = @()) {
    & winget list --id $id --exact --accept-source-agreements 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { Write-Host "$id zaten kurulu."; return }
    Write-Host "$id kuruluyor..."
    & winget install --id $id --exact --accept-package-agreements --accept-source-agreements --silent @extra
    # 0 = OK, 3010 = Reboot required (basarili), -1978335189 / -1978335135 = Zaten kurulu / guncelleme yok
    $okCodes = @(0, 3010, -1978335189, -1978335135)
    if ($okCodes -notcontains $LASTEXITCODE) { throw "$id installation failed with code $LASTEXITCODE." }
}
if (!(Get-Command winget -ErrorAction SilentlyContinue)) { throw 'Windows Package Manager (winget) is required.' }

# --- 1) Bagimliliklar ---
Install-Package 'Git.Git'
# PATH'i guncelle (Git yeni kurulmussa mevcut oturumda gorulmeyebilir)
$gitDir = "$env:ProgramFiles\Git\cmd"
if ((Test-Path $gitDir) -and $env:Path -notlike "*$gitDir*") { $env:Path = "$gitDir;$env:Path" }
try { Install-Package 'GitHub.GitLFS' } catch {
    Write-Host 'Git LFS ayri kurulamadi, Git ile gelen LFS kullanilacak.'
    $lfs = Get-Command git-lfs.exe -ErrorAction SilentlyContinue
    if (-not $lfs) {
        $lfs = Get-ChildItem "$env:ProgramFiles\Git" -Recurse -Filter 'git-lfs.exe' -ErrorAction SilentlyContinue | Select-Object -First 1
    }
    if ($lfs) { Write-Host "git-lfs bulundu: $($lfs)" }
}
Install-Package 'Microsoft.VCRedist.2015+.x86'
Install-Package 'Microsoft.DotNet.Framework.DeveloperPack_4'

# VS2022 C++ BuildTools kontrolu (VS Community/Enterprise veya BuildTools icinde cl.exe varsa tekrar indirme)
$vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
$hasCl = $false
if (Test-Path $vswhere) {
    $clHit = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -find 'VC\Tools\MSVC\**\bin\**\cl.exe' 2>$null | Select-Object -First 1
    if ($clHit) { $hasCl = $true; Write-Host "Visual Studio C++ derleyicisi hazir: $clHit" }
}
if (-not $hasCl) {
    Install-Package 'Microsoft.VisualStudio.2022.BuildTools' @('--override','--wait --passive --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended')
}
Install-Package 'PHP.PHP.8.3'

# PHP uzantilari (curl, intl, mbstring, openssl, pdo_mysql, mysqli, gd, fileinfo)
$phpExe = Get-PhpExe
if ($phpExe) {
    $phpDir = Split-Path $phpExe
    $phpIni = Join-Path $phpDir 'php.ini'
    if (!(Test-Path $phpIni)) {
        $prod = Join-Path $phpDir 'php.ini-production'
        if (Test-Path $prod) { Copy-Item $prod $phpIni }
    }
    if (Test-Path $phpIni) {
        $content = Read-TextStripBom $phpIni
        $extDir = (Join-Path $phpDir 'ext') -replace '\\','/'
        $content = $content -replace ';\s*extension_dir\s*=\s*"ext"', "extension_dir = `"$extDir`""
        foreach ($ext in 'curl','intl','mbstring','openssl','pdo_mysql','mysqli','gd','fileinfo') {
            $content = $content -replace ";\s*extension=$ext", "extension=$ext"
        }
        Write-Utf8NoBom $phpIni $content
        Write-Host 'PHP uzantilari etkinlestirildi.'
    }
}

Install-Package 'Python.Python.3.12'
Install-Package 'Python.Python.2' # Client Cython build (C:\Python27) gerektirir
if (-not (Test-Path 'C:\Python27\python.exe')) {
    $py27Hit = Get-ChildItem "$env:LOCALAPPDATA\Programs\Python\Python27*","$env:ProgramFiles\Python27*","${env:ProgramFiles(x86)}\Python27*" -Filter 'python.exe' -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($py27Hit) {
        New-Item -ItemType Junction -Path 'C:\Python27' -Target $py27Hit.DirectoryName -ErrorAction SilentlyContinue | Out-Null
    }
}

# --- 2) .env (otomatik uretim ve baska makineden tasinmissa IP/yol onarimi) ---
$settings = Ensure-ValidEnvForMachine

# --- 3) MariaDB (portable 11.4) - proje icinde ---
$rootPassword = $settings['MARIADB_ROOT_PASSWORD']
$mariaDir = Get-MariaDbDir
New-Item -ItemType Directory -Force -Path $mariaDir | Out-Null
if (-not (Test-Path "$mariaDir\bin\mariadbd.exe")) {
    Write-Host 'MariaDB 11.4 portable indiriliyor...'
    $mariaZip = Join-Path $env:TEMP 'mariadb-11.4.zip'
    Invoke-WebRequest 'https://archive.mariadb.org/mariadb-11.4.8/winx64-packages/mariadb-11.4.8-winx64.zip' -OutFile $mariaZip -UseBasicParsing
    Expand-Archive $mariaZip $env:TEMP\mariadb-extract -Force
    $inner = Get-ChildItem "$env:TEMP\mariadb-extract" -Directory | Select-Object -First 1
    if ($inner) { Get-ChildItem $inner.FullName | Move-Item -Destination $mariaDir -Force }
    Remove-Item $mariaZip, "$env:TEMP\mariadb-extract" -Recurse -Force -ErrorAction SilentlyContinue
}
if (-not (Test-Path "$mariaDir\data\mysql")) {
    Write-Host 'MariaDB veritabani olusturuluyor...'
    if (Test-Path "$mariaDir\data") { Remove-Item "$mariaDir\data" -Recurse -Force -ErrorAction SilentlyContinue }
    & "$mariaDir\bin\mariadb-install-db.exe" --datadir="$mariaDir\data" --password="$rootPassword"
    if ($LASTEXITCODE -ne 0) { throw 'MariaDB install-db failed.' }
}
Optimize-HardwareConfig | Out-Null
if (-not (Get-Service -Name 'MariaDB' -ErrorAction SilentlyContinue)) {
    & "$mariaDir\bin\mariadbd.exe" --install MariaDB --defaults-file="$mariaDir\data\my.ini"
} else {
    $expectedBin = "`"$mariaDir\bin\mariadbd.exe`" --defaults-file=`"$mariaDir\data\my.ini`" MariaDB"
    & sc.exe config MariaDB binPath= $expectedBin | Out-Null
}
$svc = Get-Service -Name 'MariaDB' -ErrorAction SilentlyContinue
if ($svc -and $svc.Status -ne 'Running') { Start-Service MariaDB }
Write-Host 'MariaDB 11.4 hazir.'

# --- 4) Git LFS ---
$git = Get-Command git.exe -ErrorAction SilentlyContinue
if (!$git) { $env:Path = "$env:ProgramFiles\Git\cmd;$env:Path"; $git = Get-Command git.exe -ErrorAction Stop }
Push-Location $root
& $git.Source lfs install --local
& $git.Source lfs pull
Pop-Location
if ($LASTEXITCODE -ne 0) { throw "Git LFS download failed with code $LASTEXITCODE." }

# --- 5) Nginx - proje icinde ---
$nginxDir = Get-NginxDir
New-Item -ItemType Directory -Force -Path $nginxDir | Out-Null
if (-not (Get-NginxExe)) {
    Write-Host 'nginx indiriliyor...'
    $zip = Join-Path $env:TEMP 'nginx.zip'
    Invoke-WebRequest 'https://nginx.org/download/nginx-1.27.5.zip' -OutFile $zip -UseBasicParsing
    Expand-Archive $zip "$env:TEMP\nginx-extract" -Force
    $inner = Get-ChildItem "$env:TEMP\nginx-extract" -Directory | Select-Object -First 1
    if ($inner) { Get-ChildItem $inner.FullName | Move-Item -Destination $nginxDir -Force }
    Remove-Item $zip, "$env:TEMP\nginx-extract" -Recurse -Force -ErrorAction SilentlyContinue
}
# SSL sertifika - Let's Encrypt IP sertifikasi (lego, shortlived profil) -> runtime\dependencies\nginx\certs altinda
$certDir = Join-Path $nginxDir 'certs'
New-Item -ItemType Directory -Force -Path $certDir | Out-Null
$certPem = Join-Path $certDir 'cert.pem'; $keyPem = Join-Path $certDir 'key.pem'
$legoDir = Join-Path $root 'runtime\dependencies\lego'
$legoExe = Join-Path $legoDir 'lego.exe'
$legoStore = Join-Path $certDir 'lego'
$cn = if ($settings.PUBLIC_IP) { $settings.PUBLIC_IP } else { 'localhost' }
# lego indir (yoksa)
if (-not (Test-Path $legoExe)) {
    $legoVer = '5.3.1'
    $legoZip = Join-Path $env:TEMP 'lego.zip'
    $legoUrl = "https://github.com/go-acme/lego/releases/download/v${legoVer}/lego_v${legoVer}_windows_amd64.zip"
    Write-Host "lego indiriliyor ($legoVer)..."
    Invoke-WebRequest $legoUrl -OutFile $legoZip -UseBasicParsing
    New-Item -ItemType Directory -Force -Path $legoDir | Out-Null
    Expand-Archive $legoZip -DestinationPath $legoDir -Force
    Remove-Item $legoZip -ErrorAction SilentlyContinue
}
if (-not (Test-Path $certPem)) {
    # nginx durdur (80 portu lazim)
    Get-Process nginx -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 2
    Write-Host "Let's Encrypt IP sertifikasi aliniyor ($cn)..."
    & $legoExe run --email="admin@valiant2.com" --accept-tos --http --http.address=":80" --domains="$cn" --path="$legoStore" --profile="shortlived"
    if ($LASTEXITCODE -eq 0) {
        $legoCert = Join-Path $legoStore "certificates\$cn.crt"
        $legoKey  = Join-Path $legoStore "certificates\$cn.key"
        Copy-Item $legoCert $certPem -Force
        Copy-Item $legoKey  $keyPem  -Force
        Write-Host "Let's Encrypt sertifikasi alindi ve deploy edildi."
    } else {
        Write-Host "Let's Encrypt basarisiz - self-signed fallback..."
        $openssl = Get-ChildItem "$env:ProgramFiles\Git\usr\bin\openssl.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($openssl) {
            $sanConf = Join-Path $certDir 'san.cnf'
            $sanText = @"
[req]
default_bits=2048
prompt=no
default_md=sha256
distinguished_name=dn
x509_extensions=v3_req
[dn]
CN=$cn
[v3_req]
subjectAltName=IP:$cn,DNS:localhost,IP:127.0.0.1
"@
            Write-Utf8NoBom $sanConf $sanText
            & $openssl.FullName req -x509 -newkey rsa:2048 -nodes -keyout $keyPem -out $certPem -days 3650 -config $sanConf
            Remove-Item $sanConf -ErrorAction SilentlyContinue
            Write-Host "Self-signed sertifika uretildi ($cn)."
        }
    }
}
# Otomatik yenileme gorevi (her 4 gunde, sertifika 6 gun gecerli)
$renewScript = Join-Path $root 'scripts\windows\renew-cert.ps1'
$renewText = @"
`$root = Split-Path (Split-Path `$PSScriptRoot)
. (Join-Path `$root 'scripts\windows\common.ps1')
`$settings = Get-EnvSettings
`$cn = `$settings.PUBLIC_IP
`$legoExe = Join-Path `$root 'runtime\dependencies\lego\lego.exe'
`$certDir = Join-Path (Get-NginxDir) 'certs'
`$legoStore = Join-Path `$certDir 'lego'
Get-Process nginx -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep 2
& `$legoExe run --email='admin@valiant2.com' --accept-tos --http --http.address=':80' --domains=`$cn --path=`$legoStore --profile='shortlived' --renew-force
if (`$LASTEXITCODE -eq 0) {
    Copy-Item (Join-Path `$legoStore "certificates\`$cn.crt") (Join-Path `$certDir 'cert.pem') -Force
    Copy-Item (Join-Path `$legoStore "certificates\`$cn.key") (Join-Path `$certDir 'key.pem') -Force
}
& (Join-Path `$root 'scripts\windows\start-stack.ps1')
"@
Write-Utf8NoBom $renewScript $renewText
$taskName = 'LegoIPRenew'
$existTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if (-not $existTask) {
    $action  = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$renewScript`""
    $trigger = New-ScheduledTaskTrigger -Daily -DaysInterval 4 -At '04:00'
    $principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Description 'Renew Let''s Encrypt IP certificate (shortlived)' | Out-Null
    Write-Host "Sertifika yenileme gorevi olusturuldu ($taskName)."
}
# nginx.conf'u canli degerlerle yaz (sablon dosyasi yok)
$certF = $certPem -replace '\\','/'; $keyF = $keyPem -replace '\\','/'
$nginxConf = @"
worker_processes  1;

events {
    worker_connections  8192;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    server_tokens   off;

    limit_req_zone `$binary_remote_addr zone=panel:10m rate=50r/s;

    upstream panel_backend {
        server 127.0.0.1:8090;
        server 127.0.0.1:8092;
        server 127.0.0.1:8093;
        server 127.0.0.1:8094;
    }

    server {
        listen 80;
        server_name _;
        return 301 https://`$host`$request_uri;
    }

    server {
        listen 443 ssl;
        server_name _;

        ssl_certificate     $certF;
        ssl_certificate_key $keyF;
        ssl_protocols       TLSv1.2 TLSv1.3;

        limit_req zone=panel burst=100 nodelay;

        location /patcher/ {
            proxy_pass http://127.0.0.1:8091;
            proxy_set_header Host `$host;
            proxy_read_timeout 600s;
        }

        location /update/ {
            proxy_pass http://127.0.0.1:8091;
            proxy_set_header Host `$host;
            proxy_read_timeout 600s;
            proxy_buffering off;
        }

        location / {
            proxy_pass http://panel_backend;
            proxy_set_header Host `$host;
            proxy_set_header X-Real-IP `$remote_addr;
            proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
            proxy_read_timeout 60s;
        }
    }
}
"@
[IO.File]::WriteAllText((Join-Path $nginxDir 'conf\nginx.conf'), $nginxConf, [Text.UTF8Encoding]::new($false))
& (Join-Path $nginxDir 'nginx.exe') -t -p $nginxDir
if ($LASTEXITCODE -ne 0) { throw 'nginx.conf testi basarisiz.' }

# --- 6) Patchserver dagitimi ---
$patchRoot = Get-PatchRoot $settings
New-Item -ItemType Directory -Force -Path "$patchRoot\patch\files", "$patchRoot\patcher" | Out-Null
foreach ($f in 'file_server.py','patch_watch.py') {
    Copy-Item (Join-Path $root "source\patchserver\$f") (Join-Path $patchRoot $f) -Force
}
$patchCfgJson = @{
    game_dir    = (Join-Path $root 'runtime\client\game')
    patch_dir   = "$patchRoot\patch"
    patcher_dir = "$patchRoot\patcher"
    base_url    = (Get-PublicBase $settings)
} | ConvertTo-Json
Write-Utf8NoBom (Join-Path $patchRoot 'patchserver.json') $patchCfgJson
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

# --- 9b) Yonetici hesabi + GM yetkisi (istege bagli) ---
if (-not $NonInteractive -and -not [Console]::IsInputRedirected) {
    Write-Host ''
    & (Join-Path $PSScriptRoot 'create-account.ps1')
}

# --- 9c) Bozuk symlink referanslarini duzelt (Git/Windows uyumsuzlugu) ---
$pyExe = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($pyExe) {
    & $pyExe (Join-Path $PSScriptRoot 'fix-symlinks.py')
}

& (Join-Path $PSScriptRoot 'build-all.ps1')
& (Join-Path $PSScriptRoot 'build-patcher.ps1')
& (Join-Path $PSScriptRoot 'build-control-center.ps1')

# --- 9c) Uretilen dosyalari git diff'inden gizle ---
& (Join-Path $PSScriptRoot 'git-sanitize.ps1')

# --- 10) Her seyi baslat ---
& (Join-Path $PSScriptRoot 'start-stack.ps1')
& (Join-Path $PSScriptRoot 'start-server.ps1')

Write-Host ''
Write-Host 'VALIANT2 setup completed - stack ve oyun sunucusu baslatildi.'
Write-Host "Durum kontrolu: $PSScriptRoot\stack-status.cmd"
