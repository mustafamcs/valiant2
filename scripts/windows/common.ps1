# Ortak yardimcilar — tum scriptler buradan .env okur ve araclari bulur.
# Kullanim: . (Join-Path $PSScriptRoot 'common.ps1')

$script:ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

function Get-EnvSettings {
    $envFile = Join-Path $script:ProjectRoot '.env'
    $s = @{}
    if (Test-Path $envFile) {
        Get-Content $envFile | ForEach-Object {
            $line = $_.Trim()
            if ($line -and !$line.StartsWith('#') -and $line.Contains('=')) {
                $k, $v = $line.Split('=', 2)
                $s[$k.Trim()] = $v.Trim().Trim('"').Trim("'")
            }
        }
    }
    return $s
}

function Get-PublicBase {
    param($Settings)
    $ip = $Settings['PUBLIC_IP']; if (-not $ip) { $ip = $Settings['CLIENT_SERVER_IP'] }
    if (-not $ip) { $ip = '127.0.0.1' }
    return "https://$ip"
}

function Get-PatchRoot {
    param($Settings)
    $p = $Settings['PATCH_ROOT']; if (-not $p) { $p = 'C:\patchserver' }
    return $p
}

function Get-PhpExe {
    $cmd = Get-Command php.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $hit = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages","$env:ProgramFiles","${env:ProgramFiles(x86)}" -Recurse -Filter php.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($hit) { return $hit.FullName }
    throw 'php.exe bulunamadi (winget install PHP.PHP.8.3)'
}

function Get-PythonwExe {
    $cmd = Get-Command pythonw.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $hit = Get-ChildItem "$env:LOCALAPPDATA\Programs\Python","$env:ProgramFiles\Python*","${env:ProgramFiles(x86)}\Python*" -Recurse -Filter pythonw.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($hit) { return $hit.FullName }
    throw 'pythonw.exe bulunamadi (winget install Python.Python.3.12)'
}

function Get-MysqlClient {
    foreach ($name in 'mariadb.exe','mysql.exe') {
        $cmd = Get-Command $name -ErrorAction SilentlyContinue
        if ($cmd) { return $cmd.Source }
    }
    $hit = Get-ChildItem "$env:ProgramFiles\MariaDB*\bin","C:\usr\bin" -Include 'mariadb.exe','mysql.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($hit) { return $hit.FullName }
    return $null
}

function Get-NginxExe {
    $hit = Get-ChildItem 'C:\nginx*' -Directory -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First 1
    if ($hit -and (Test-Path (Join-Path $hit.FullName 'nginx.exe'))) { return (Join-Path $hit.FullName 'nginx.exe') }
    $cmd = Get-Command nginx.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    return $null
}
