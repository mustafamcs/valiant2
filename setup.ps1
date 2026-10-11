$ErrorActionPreference = 'Stop'
$principal = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
if (!$principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell.exe -Verb RunAs -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$PSCommandPath`"") -Wait
    exit $LASTEXITCODE
}
$root = Split-Path -Parent $PSCommandPath
function Install-Package([string]$id, [string[]]$extra = @()) {
    & winget list --id $id --exact --accept-source-agreements | Out-Null
    if ($LASTEXITCODE -eq 0) { return }
    & winget install --id $id --exact --accept-package-agreements --accept-source-agreements --silent @extra
    if ($LASTEXITCODE -ne 0) { throw "$id installation failed with code $LASTEXITCODE." }
}
if (!(Get-Command winget -ErrorAction SilentlyContinue)) { throw 'Windows Package Manager (winget) is required.' }
Install-Package 'Git.Git'
Install-Package 'GitHub.GitLFS'
Install-Package 'Microsoft.VCRedist.2015+.x86'
Install-Package 'Microsoft.DotNet.Framework.DeveloperPack_4'
Install-Package 'Microsoft.VisualStudio.2022.BuildTools' @('--override','--wait --passive --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended')
$envFile = Join-Path $root '.env'
if (!(Test-Path $envFile)) {
    $dbPassword = ([guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N'))
    $adminPassword = [guid]::NewGuid().ToString('N')
    $rootPassword = ([guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N'))
    $content = Get-Content (Join-Path $root '.env.example') -Raw
    $content = $content -replace '(?m)^MYSQL_PASSWORD=.*$', "MYSQL_PASSWORD=$dbPassword"
    $content = $content -replace '(?m)^ADMINPAGE_PASSWORD=.*$', "ADMINPAGE_PASSWORD=$adminPassword"
    $content = $content -replace '(?m)^MARIADB_ROOT_PASSWORD=.*$', "MARIADB_ROOT_PASSWORD=$rootPassword"
    [IO.File]::WriteAllText($envFile, $content, [Text.UTF8Encoding]::new($false))
}
$rootPassword = (Get-Content $envFile | Where-Object { $_ -match '^MARIADB_ROOT_PASSWORD=' } | Select-Object -First 1).Split('=',2)[1]
Install-Package 'MariaDB.Server' @('--override',"SERVICENAME=MariaDB PASSWORD=$rootPassword /qn")
$git = Get-Command git.exe -ErrorAction SilentlyContinue
if (!$git) {
    $env:Path = "$env:ProgramFiles\Git\cmd;$env:Path"
    $git = Get-Command git.exe -ErrorAction Stop
}
& $git.Source lfs install --local
& $git.Source lfs pull
if ($LASTEXITCODE -ne 0) { throw "Git LFS download failed with code $LASTEXITCODE." }
& (Join-Path $root 'scripts\windows\setup-database.ps1')
& (Join-Path $root 'scripts\windows\build-all.ps1')
Write-Host 'VALIANT2 setup completed.'
Write-Host 'Start the server with scripts\windows\start-server.cmd and the client with runtime\client\M2Client.exe.'
