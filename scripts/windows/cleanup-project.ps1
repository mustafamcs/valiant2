param([switch]$RestartServer)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$serverWasRunning = Test-Path (Join-Path $root 'runtime\server\.state\valiant-db.pid')
if ($serverWasRunning) { & (Join-Path $PSScriptRoot 'stop-server.ps1') }
$allFiles = Get-ChildItem $root -Recurse -Force -File -ErrorAction SilentlyContinue
$targets = $allFiles | Where-Object {
    $path = $_.FullName
    $name = $_.Name
    $extension = $_.Extension
    $runtimeGarbage = $path -match '\\(logs|syserr|GPUCache|screenshot)\\' -or $name -match '^(syslog|syserr|stdout|profile|packet_info|p2p_packet_info)(\.txt)?$'
    $buildGarbage = $extension -in @('.obj','.tlog','.lastbuildstate','.recipe','.ipdb','.iobj','.pch','.ilk','.idb','.bsc','.aps','.res','.exp','.pdb','.map') -or (($path -match '\\(Debug|Release|OBJDIR|int)\\') -and $extension -notin @('.lib','.exe','.dll','.pak','.cpp','.c','.h','.hpp','.py','.vcxproj','.sln'))
    $generatedGarbage = $path -match '\\cyTemp\\' -or $extension -eq '.pyc' -or $path -match '\\__pycache__\\'
    $legacyMetadata = $name -in @('Not.txt','Darkmmo.url') -or $extension -in @('.scc','.vssscc','.vspscc','.suo','.user','.bak')
    $legacyUnix = $name -in @('Makefile','makefile') -or $extension -in @('.sh','.a') -or $path -match '\\runtime\\server\\main\\srv1\\share\\bin\\(game|db)$'
    $runtimeGarbage -or $buildGarbage -or $generatedGarbage -or $legacyMetadata -or $legacyUnix
} | Sort-Object FullName -Unique
$bytes = ($targets | Measure-Object Length -Sum).Sum
$count = $targets.Count
$targets | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem $root -Recurse -Force -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -in @('GPUCache','Debug','OBJDIR','__pycache__','cyTemp') -and -not (Get-ChildItem $_.FullName -Force -ErrorAction SilentlyContinue) } |
    Sort-Object { $_.FullName.Length } -Descending |
    Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem "$root\assets\unpacked\data" -Directory -Recurse -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match '(?i)(\s-\s*Copy|\s-\s*Kopya|Yeni klas)' } |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem "$root\assets","$root\source","$root\tools","$root\web" -File -Recurse -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match '(?i)(\s-\s*Copy|\s-\s*Kopya|Yeni Metin Belgesi)' } |
    Remove-Item -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $root '.lego'), (Join-Path $root 'logs'), (Join-Path $root 'deploy'), (Join-Path $root 'assets\unpacked\logs'), (Join-Path $root 'runtime\patchserver\src'), (Join-Path $root 'source\patchserver\src\VALIANT2.exe'), (Join-Path $root 'tools\client-config\config.exe'), (Join-Path $root 'web\adminpanel\start_panel.vbs') -Recurse -Force -ErrorAction SilentlyContinue
[pscustomobject]@{ DeletedFiles=$count; FreedMB=[math]::Round($bytes/1MB,2) } | Format-List
if ($RestartServer -or $serverWasRunning) { & (Join-Path $PSScriptRoot 'start-server.ps1') }
