<#
.SYNOPSIS
    VALIANT2 Coklu Dil (Multi-Language) Anahtar Ekleme / Guncelleme Araci
.DESCRIPTION
    Python root/uiscript dosyalarina sabit (hardcoded) metin veya \xfc gibi kacis dizileri
    yazmak yerine 8 dilin (tr, en, de, it, ro, pl, cz, hu) locale_interface_custom.txt ve
    locale_game_custom.txt dosyalarina dogru kod sayfasinda (CP1254 / CP1250) anahtar ekler.
#>
param(
    [string]$Key,
    [string]$Tr,
    [string]$En,
    [string]$De = '',
    [string]$It = '',
    [string]$Ro = '',
    [string]$Pl = '',
    [string]$Cz = '',
    [string]$Hu = '',
    [string]$JsonFile = '',
    [switch]$BuildPack
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
. (Join-Path $PSScriptRoot 'common.ps1')

$langEncodings = @{
    'tr' = 1254
    'en' = 1254
    'de' = 1254
    'it' = 1254
    'ro' = 1250
    'pl' = 1250
    'cz' = 1250
    'hu' = 1250
}

$entries = @{}
if ($JsonFile -and (Test-Path $JsonFile)) {
    $parsed = Get-Content $JsonFile -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($prop in $parsed.PSObject.Properties) {
        $entries[$prop.Name] = $prop.Value
    }
} elseif ($Key -and $Tr) {
    if (-not $En) { $En = $Tr }
    $entries[$Key] = [PSCustomObject]@{
        tr = $Tr
        en = $En
        de = if ($De) { $De } else { $En }
        it = if ($It) { $It } else { $En }
        ro = if ($Ro) { $Ro } else { $En }
        pl = if ($Pl) { $Pl } else { $En }
        cz = if ($Cz) { $Cz } else { $En }
        hu = if ($Hu) { $Hu } else { $En }
    }
} else {
    throw "Kullanim: .\add-locale-string.ps1 -Key 'ANAHTAR_ADI' -Tr 'Turkce Metin' -En 'English Text' [-BuildPack]"
}

$localeRoot = Join-Path $root 'assets\unpacked\data\locale'
foreach ($lang in $langEncodings.Keys) {
    $cp = $langEncodings[$lang]
    $enc = [System.Text.Encoding]::GetEncoding($cp)
    foreach ($fileName in @('locale_interface_custom.txt', 'locale_game_custom.txt')) {
        $filePath = Join-Path (Join-Path $localeRoot $lang) $fileName
        if (-not (Test-Path $filePath)) { continue }

        $rawBytes = [System.IO.File]::ReadAllBytes($filePath)
        $text = $enc.GetString($rawBytes)
        $lines = $text -split "\r?\n"
        $kept = New-Object System.Collections.Generic.List[string]

        foreach ($line in $lines) {
            if ([string]::IsNullOrWhiteSpace($line)) { continue }
            $tok = ($line -split "`t")[0].Trim()
            if (-not $entries.ContainsKey($tok)) {
                $kept.Add($line)
            }
        }

        foreach ($k in $entries.Keys) {
            $valObj = $entries[$k]
            $val = $valObj.$lang
            if (-not $val) { $val = $valObj.en }
            if (-not $val) { $val = $valObj.tr }
            $kept.Add("$k`t$val")
        }

        $outText = ($kept -join "`r`n") + "`r`n"
        [System.IO.File]::WriteAllBytes($filePath, $enc.GetBytes($outText))
    }
}

Write-Host ("{0} adet coklu dil anahtari 8 dile (CP1254/CP1250) basariyla islendi." -f $entries.Count) -ForegroundColor Green

if ($BuildPack) {
    & (Join-Path $PSScriptRoot 'build-client-packs.ps1') -Archive locale
}
