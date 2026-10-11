param(
    [string[]]$Flags = @(),
    [switch]$AllOff,
    [switch]$ServerOnly,
    [switch]$ClientOnly
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$clientHeader = Join-Path $root 'source\client\source\Controls.h'
$serverHeader = Join-Path $root 'source\server\source\common\Controls.h'
$msbuild = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe'
$featurePattern = '^\s*#define\s+((?:ENABLE|WJ|USE)_[A-Za-z0-9_]+|__[A-Za-z0-9_]+__)\b'
function Get-Flags([string]$path) {
    $regex = [regex]::new($featurePattern)
    foreach ($line in [IO.File]::ReadAllLines($path)) {
        $match = $regex.Match($line)
        if ($match.Success) { $match.Groups[1].Value }
    }
}
function Disable-Flags([string]$path, [string[]]$names) {
    $set = @{}; foreach ($name in $names) { $set[$name] = $true }
    $regex = [regex]::new($featurePattern)
    $lines = [IO.File]::ReadAllLines($path)
    for ($i = 0; $i -lt $lines.Length; ++$i) {
        $match = $regex.Match($lines[$i])
        if ($match.Success -and $set.ContainsKey($match.Groups[1].Value)) {
            $lines[$i] = $lines[$i] -replace '^(\s*)#define', '$1//#define'
        }
    }
    [IO.File]::WriteAllLines($path, $lines)
}
$clientBackup = [IO.File]::ReadAllBytes($clientHeader)
$serverBackup = [IO.File]::ReadAllBytes($serverHeader)
try {
    $clientFlags = @(Get-Flags $clientHeader | Sort-Object -Unique)
    $serverFlags = @(Get-Flags $serverHeader | Sort-Object -Unique)
    if ($AllOff) {
        $selectedClient = $clientFlags
        $selectedServer = $serverFlags
    } elseif ($Flags.Count) {
        $selectedClient = @($Flags | Where-Object { $clientFlags -contains $_ })
        $selectedServer = @($Flags | Where-Object { $serverFlags -contains $_ })
    } else {
        throw 'Specify -AllOff or -Flags.'
    }
    if (!$ServerOnly) { Disable-Flags $clientHeader $selectedClient }
    if (!$ClientOnly) { Disable-Flags $serverHeader $selectedServer }
    Write-Host "Disabled client flags: $($selectedClient.Count)"
    Write-Host "Disabled server flags: $($selectedServer.Count)"
    $results = @()
    if (!$ClientOnly) {
        & $msbuild (Join-Path $root 'source\server\source\AntrumServer.sln') /t:Rebuild /m /p:Configuration=Release /p:Platform=Win32 /v:minimal
        $results += [pscustomobject]@{ Target='server'; ExitCode=$LASTEXITCODE }
    }
    if (!$ServerOnly) {
        & $msbuild (Join-Path $root 'source\client\external\projects\UserInterface\UserInterface.vcxproj') /m /p:Configuration=Release /p:Platform=Win32 /p:BuildProjectReferences=false /v:minimal
        $results += [pscustomobject]@{ Target='client'; ExitCode=$LASTEXITCODE }
    }
    $results | Format-Table -AutoSize
    if ($results.ExitCode -contains 1) { exit 1 }
} finally {
    [IO.File]::WriteAllBytes($clientHeader, $clientBackup)
    [IO.File]::WriteAllBytes($serverHeader, $serverBackup)
}
