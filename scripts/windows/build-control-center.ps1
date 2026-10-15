# VALIANT2 Control Center (VALIANT2-ControlCenter.exe) derler ve proje kokune yerlestirir.
# Windows icindeki dahili .NET Framework 4 csc.exe kullanir - VS2022 kurulmadan once bile (sifir makinede) derlenebilir.
param([switch]$ForceKill)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
. (Join-Path $PSScriptRoot 'common.ps1')
$srcDir = Join-Path $root 'tools\control-center'
$outExe = Join-Path $root 'VALIANT2-ControlCenter.exe'
$ico = Join-Path $root 'tools\branding\valiant2.ico'
$logo = Join-Path $root 'source\patchserver\src\logo.png'
$manifest = Join-Path $srcDir 'app.manifest'
$csc = Get-CscExe

$runningCc = Get-Process -Name 'VALIANT2-ControlCenter' -ErrorAction SilentlyContinue
if ($runningCc -and $ForceKill) {
    $runningCc | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Milliseconds 300
    $runningCc = $null
}

$targetOut = if ($runningCc) { Join-Path $root 'VALIANT2-ControlCenter.new.exe' } else { $outExe }

$sources = @(
    (Join-Path $srcDir 'Program.cs'),
    (Join-Path $srcDir 'Theme.cs'),
    (Join-Path $srcDir 'BackendService.cs'),
    (Join-Path $srcDir 'ControlCenterForm.cs'),
    (Join-Path $srcDir 'Pages\DashboardPage.cs'),
    (Join-Path $srcDir 'Pages\SetupWizardPage.cs'),
    (Join-Path $srcDir 'Pages\BuildPackPage.cs'),
    (Join-Path $srcDir 'Pages\DatabaseGmPage.cs'),
    (Join-Path $srcDir 'Pages\ConfigGitPage.cs')
)

# csc.exe Turkce karakterleri ve sembolleri dogru okumasi icin UTF-8 BOM garanti et
$utf8Bom = New-Object System.Text.UTF8Encoding($true)
foreach ($f in $sources) {
    $txt = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
    [System.IO.File]::WriteAllText($f, $txt, $utf8Bom)
}

& $csc /nologo /target:winexe /optimize+ /out:"$targetOut" /win32icon:"$ico" /win32manifest:"$manifest" /res:"$logo,logo.png" `
    /r:System.dll /r:System.Core.dll /r:System.Drawing.dll /r:System.Windows.Forms.dll /r:System.Net.dll /r:System.ServiceProcess.dll `
    $sources

if ($LASTEXITCODE -ne 0) { throw "VALIANT2-ControlCenter derleme hatasi: $LASTEXITCODE" }
if ($targetOut -ne $outExe) {
    try {
        Move-Item $targetOut $outExe -Force -ErrorAction Stop
    } catch {
        Remove-Item $targetOut -Force -ErrorAction SilentlyContinue
    }
}
Write-Host "VALIANT2-ControlCenter.exe basariyla derlendi: $outExe"
