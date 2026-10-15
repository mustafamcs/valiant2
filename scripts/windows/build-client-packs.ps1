param([string]$Archive = 'all', [switch]$Force)
$ErrorActionPreference = 'Stop'
$sw = [Diagnostics.Stopwatch]::StartNew()
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Get-Process -Name 'M2Client' -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
$assets = Join-Path $root 'assets\unpacked'
$archiver = Join-Path $assets 'FSArchiver.exe'
$runtimePack = Join-Path $root 'runtime\client\game\pack'
New-Item -ItemType Directory -Force -Path $runtimePack | Out-Null

$normArchive = if ($Archive -eq 'all') { 'all' } else { Split-Path -Leaf ($Archive -replace '^data[/\\]', '') }

if (-not ('FastPackChecker' -as [type])) {
    Add-Type -TypeDefinition @"
using System;
using System.Collections.Concurrent;
using System.IO;
using System.Threading.Tasks;

public static class FastPackChecker {
    public static bool IsDirNewerThan(string dirPath, DateTime pakUtc) {
        if (!Directory.Exists(dirPath)) return false;
        foreach (string f in Directory.EnumerateFiles(dirPath, "*", SearchOption.AllDirectories)) {
            if (File.GetLastWriteTimeUtc(f) > pakUtc) return true;
        }
        return false;
    }
    public static string[] FindOutdatedPacks(string assetsDir, string[] dirs, string[] pakRels) {
        var result = new ConcurrentBag<string>();
        Parallel.For(0, dirs.Length, i => {
            string dirRel = dirs[i];
            string packName = Path.GetFileName(dirRel.TrimEnd('/', '\\'));
            string pakFull = Path.GetFullPath(Path.Combine(assetsDir, pakRels[i].Replace('/', '\\')));
            if (!File.Exists(pakFull)) {
                result.Add(packName);
                return;
            }
            DateTime pakUtc = File.GetLastWriteTimeUtc(pakFull);
            string srcFull = Path.Combine(assetsDir, dirRel.Replace('/', '\\'));
            if (IsDirNewerThan(srcFull, pakUtc)) {
                result.Add(packName);
            }
        });
        var arr = result.ToArray();
        Array.Sort(arr, StringComparer.OrdinalIgnoreCase);
        return arr;
    }
}
"@
}

Push-Location $assets
try {
    $cfgList = Get-Content (Join-Path $assets 'config.json') -Raw | ConvertFrom-Json
    $expectedPaks = @{}
    foreach ($c in $cfgList) {
        $expectedPaks[(Split-Path -Leaf $c.file).ToLower()] = $true
    }
    Get-ChildItem $runtimePack -File -Filter '*.pak' -ErrorAction SilentlyContinue | Where-Object { -not $expectedPaks.ContainsKey($_.Name.ToLower()) } | Remove-Item -Force -ErrorAction SilentlyContinue

    if ($normArchive -eq 'all' -and -not $Force) {
        $dirs = [string[]]@($cfgList | ForEach-Object { $_.dir })
        $paks = [string[]]@($cfgList | ForEach-Object { $_.file })
        $toBuild = @([FastPackChecker]::FindOutdatedPacks($assets, $dirs, $paks))

        if ($toBuild.Count -eq 0) {
            Write-Host "Tum $($dirs.Count) client pack arsivi guncel (degisen dosya yok)."
        } elseif ($toBuild.Count -ge 50) {
            Write-Host "Toplu pack uretimi baslatildi ($($toBuild.Count) arsiv, 32 thread)..."
            & $archiver 'config.json' 'all' > $null
            if ($LASTEXITCODE -ne 0) { throw "FSArchiver failed with code $LASTEXITCODE." }
        } else {
            foreach ($arc in $toBuild) {
                Write-Host "Degisen pack guncelleniyor: $arc.pak"
                & $archiver 'config.json' $arc > $null
                if ($LASTEXITCODE -ne 0) { throw "FSArchiver failed on $arc with code $LASTEXITCODE." }
            }
        }
    } else {
        Write-Host "FSArchiver calisiyor ($normArchive)..."
        & $archiver 'config.json' $normArchive > $null
        if ($LASTEXITCODE -ne 0) { throw "FSArchiver failed with code $LASTEXITCODE." }
    }
} finally {
    Pop-Location
    Remove-Item (Join-Path $assets 'logs'), (Join-Path $root 'logs') -Recurse -Force -ErrorAction SilentlyContinue
}
$sw.Stop()
$el = [math]::Round($sw.Elapsed.TotalSeconds, 2)
Write-Host "Client packs tamamlandi ($el sn)."
