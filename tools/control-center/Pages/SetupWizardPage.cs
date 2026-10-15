using System;
using System.Collections.Generic;
using System.Drawing;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Valiant2ControlCenter.Pages
{
    internal sealed class SetupWizardPage : BufferedPanel
    {
        private readonly BackendService backend;
        private readonly Panel stepsPanel;
        private readonly Label lblStatusSummary;

        public SetupWizardPage(BackendService backend)
        {
            this.backend = backend;
            Dock = DockStyle.Fill;
            BackColor = Theme.BgMain;
            Padding = new Padding(8, 6, 8, 6);

            var topBar = new BufferedPanel
            {
                Dock = DockStyle.Top,
                Height = 46,
                BackColor = Theme.BgCard,
                DrawCardBorder = true,
                Padding = new Padding(8, 6, 8, 6)
            };

            var btnFull = Theme.CreateButton("★ SIFIRDAN KUR", ButtonStyle.PrimaryCrimson, 200, 30);
            btnFull.Location = new Point(8, 7);
            btnFull.Click += async (s, e) => await RunFullSetup();

            var btnReset = Theme.CreateButton("🔄 KALDIR & KUR", ButtonStyle.Danger, 185, 30);
            btnReset.Location = new Point(214, 7);
            btnReset.Click += async (s, e) => await ResetAndCleanInstallAsync(true);

            var btnRepair = Theme.CreateButton("🔧 CONFIG + DB ONAR", ButtonStyle.PrimaryGold, 165, 30);
            btnRepair.Location = new Point(405, 7);
            btnRepair.Click += async (s, e) =>
            {
                await backend.RunPowerShellScriptAsync("Config & Symlink Onarımı", "sync-config.ps1");
                await backend.RunPowerShellScriptAsync("Veritabanı Şema Kurulumu", "setup-database.ps1");
                RefreshChecklist();
            };

            var btnCheck = Theme.CreateButton("↻ DENETLE", ButtonStyle.Secondary, 95, 30);
            btnCheck.Location = new Point(576, 7);
            btnCheck.Click += (s, e) => RefreshChecklist();

            lblStatusSummary = new Label
            {
                Text = "9/9 Hazır",
                Font = Theme.FontBodyBold,
                ForeColor = Theme.Emerald,
                Location = new Point(678, 13),
                Size = new Size(112, 20),
                TextAlign = ContentAlignment.MiddleRight
            };

            topBar.Controls.AddRange(new Control[] { btnFull, btnReset, btnRepair, btnCheck, lblStatusSummary });

            stepsPanel = new BufferedPanel
            {
                Dock = DockStyle.Fill,
                BackColor = Color.Transparent,
                Padding = new Padding(0, 4, 0, 0)
            };

            Controls.Add(stepsPanel);
            Controls.Add(topBar);

            RefreshChecklist();
        }

        public void RefreshChecklist()
        {
            Task.Run(() =>
            {
                var steps = backend.InspectSetupSteps();
                if (IsDisposed) return;
                BeginInvoke(new Action(() => RenderSteps(steps)));
            });
        }

        private void RenderSteps(List<SetupStepState> steps)
        {
            stepsPanel.SuspendLayout();
            stepsPanel.Controls.Clear();

            int readyCount = 0;
            int y = 4;
            int w = Math.Max(780, stepsPanel.ClientSize.Width);

            foreach (var step in steps)
            {
                if (step.IsReady) readyCount++;

                var row = new BufferedPanel
                {
                    Location = new Point(0, y),
                    Size = new Size(w, 29),
                    BackColor = Theme.BgCard,
                    DrawCardBorder = true,
                    HighlightBorder = step.IsReady
                };

                var lblDot = new Label
                {
                    Text = step.IsReady ? "✓" : "!",
                    Location = new Point(6, 4),
                    Size = new Size(20, 20),
                    TextAlign = ContentAlignment.MiddleCenter,
                    Font = Theme.FontBodyBold,
                    ForeColor = step.IsReady ? Theme.Emerald : Theme.Amber,
                    BackColor = step.IsReady ? Theme.EmeraldBg : Theme.AmberBg
                };

                var lblTitle = new Label
                {
                    Text = step.Title,
                    Font = Theme.FontBodyBold,
                    ForeColor = step.IsReady ? Theme.GoldBright : Theme.TextMain,
                    Location = new Point(32, 5),
                    Size = new Size(375, 19),
                    AutoEllipsis = true
                };

                var lblDetail = new Label
                {
                    Text = step.StatusDetail,
                    Font = Theme.FontSmall,
                    ForeColor = step.IsReady ? Theme.Emerald : Theme.Amber,
                    Location = new Point(412, 6),
                    Size = new Size(265, 18),
                    TextAlign = ContentAlignment.MiddleRight,
                    AutoEllipsis = true
                };

                var btnStep = Theme.CreateButton(step.IsReady ? "YENİLE" : "KUR",
                    step.IsReady ? ButtonStyle.Secondary : ButtonStyle.PrimaryGold, 105, 23);
                btnStep.Location = new Point(w - 112, 3);
                btnStep.Font = Theme.FontButtonSm;

                string sid = step.Id;
                string stitle = step.Title;
                btnStep.Click += async (s, e) =>
                {
                    await ExecuteSingleStep(sid, stitle);
                    RefreshChecklist();
                };

                row.Controls.AddRange(new Control[] { lblDot, lblTitle, lblDetail, btnStep });
                stepsPanel.Controls.Add(row);
                y += 31;
            }

            lblStatusSummary.Text = string.Format("{0} / {1} Hazır", readyCount, steps.Count);
            stepsPanel.ResumeLayout();
        }

        private async Task RunFullSetup()
        {
            if (MessageBox.Show("Sıfırdan Tam Kurulum (setup.ps1) başlatılsın mı?", "VALIANT2 Kurulum",
                MessageBoxButtons.YesNo, MessageBoxIcon.Question) != DialogResult.Yes) return;

            await backend.RunPowerShellInlineAsync("Sıfırdan Tam Kurulum (setup.ps1)",
                "& '" + System.IO.Path.Combine(backend.ScriptsDir, "setup.ps1") + "' -NonInteractive");
            RefreshChecklist();
        }

        public async Task ResetAndCleanInstallAsync(bool confirmWithUser)
        {
            if (confirmWithUser)
            {
                if (MessageBox.Show("Mevcut runtime bileşenleri kaldırılıp sıfırdan temiz kurulum yapılacak. Devam edilsin mi?",
                    "Kaldır & Baştan Kur", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) != DialogResult.Yes) return;
            }

            await backend.RunPowerShellScriptAsync("Oyun Sunucusu Durduruluyor", "stop-server.ps1");
            await backend.RunPowerShellScriptAsync("Web & Patch Stack Durduruluyor", "stop-stack.ps1");

            await backend.RunPowerShellInlineAsync("Mevcut Kurulum Bileşenleri Kaldırılıyor", @"
$root = '" + backend.ProjectRoot.Replace("'", "''") + @"'
Remove-Item (Join-Path $root 'runtime\dependencies\nginx') -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $root 'runtime\patchserver\patchserver.json') -Force -ErrorAction SilentlyContinue
$turkeyJunc = Join-Path $root 'runtime\server\main\srv1\share\locale\turkey'
if (Test-Path $turkeyJunc) { & cmd.exe /c ""rmdir `""$turkeyJunc`"""" 2>$null }
Remove-Item (Join-Path $root 'runtime\client\VALIANT2.exe') -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $root 'runtime\server\main\srv1\share\bin\game.exe'), (Join-Path $root 'runtime\server\main\srv1\share\bin\db.exe') -Force -ErrorAction SilentlyContinue
");
            RefreshChecklist();

            string[][] allSteps = new[]
            {
                new[] { "deps", "1. Derleme & Sistem Bağımlılıkları" },
                new[] { "env", "2. Ortam Yapılandırması (.env) & IP" },
                new[] { "mariadb", "3. MariaDB 11.4 Servisi" },
                new[] { "lfs", "4. Git LFS Dosyaları" },
                new[] { "nginx", "5. Nginx & SSL Sertifikası" },
                new[] { "patchserver", "6. Patch Sunucusu & Firewall" },
                new[] { "database", "7. Veritabanı Şemaları" },
                new[] { "symlinks", "8. Symlink & Config Onarımı" },
                new[] { "build", "9. Tam Derleme & Packler" }
            };

            foreach (var st in allSteps)
            {
                await ExecuteSingleStep(st[0], st[1]);
                RefreshChecklist();
            }

            await backend.RunPowerShellScriptAsync("Web & Patch Stack Başlatılıyor", "start-stack.ps1");
            await backend.RunPowerShellScriptAsync("Oyun Sunucusu Başlatılıyor", "start-server.ps1");
            RefreshChecklist();
        }

        public async Task ExecuteSingleStep(string stepId, string title)
        {
            switch (stepId)
            {
                case "deps":
                    await backend.RunPowerShellInlineAsync(title, @"
function Install-Package([string]$id, [string[]]$extra = @()) {
    & winget list --id $id --exact --accept-source-agreements 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { Write-Host ""$id zaten kurulu.""; return }
    & winget install --id $id --exact --accept-package-agreements --accept-source-agreements --silent @extra
    $okCodes = @(0, 3010, -1978335189, -1978335135)
    if ($okCodes -notcontains $LASTEXITCODE) { throw ""$id kurulum hatasi: $LASTEXITCODE"" }
}
Install-Package 'Git.Git'
try { Install-Package 'GitHub.GitLFS' } catch {}
Install-Package 'Microsoft.VCRedist.2015+.x86'
Install-Package 'Microsoft.DotNet.Framework.DeveloperPack_4'
$vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
$hasCl = $false
if (Test-Path $vswhere) {
    $clHit = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -find 'VC\Tools\MSVC\**\bin\**\cl.exe' 2>$null | Select-Object -First 1
    if ($clHit) { $hasCl = $true }
}
if (-not $hasCl) {
    Install-Package 'Microsoft.VisualStudio.2022.BuildTools' @('--override','--wait --passive --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended')
}
Install-Package 'PHP.PHP.8.3'
Install-Package 'Python.Python.3.12'
Install-Package 'Python.Python.2'
if (-not (Test-Path 'C:\Python27\python.exe')) {
    $py27Hit = Get-ChildItem ""$env:LOCALAPPDATA\Programs\Python\Python27*"",""$env:ProgramFiles\Python27*"",""${env:ProgramFiles(x86)}\Python27*"" -Filter 'python.exe' -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($py27Hit) { New-Item -ItemType Junction -Path 'C:\Python27' -Target $py27Hit.DirectoryName -ErrorAction SilentlyContinue | Out-Null }
}
. '" + System.IO.Path.Combine(backend.ScriptsDir, "common.ps1") + @"'
Ensure-PhpConfigured
Ensure-PanelWritableDirs
");
                    break;
                case "env":
                    await backend.RunPowerShellInlineAsync(title, @"
. '" + System.IO.Path.Combine(backend.ScriptsDir, "common.ps1") + @"'
$s = Ensure-ValidEnvForMachine -ForceRefreshIp
Write-Host "".env hazir: PUBLIC_IP=$($s['PUBLIC_IP'])""
");
                    await backend.RunPowerShellScriptAsync("Config Senkronizasyonu", "sync-config.ps1");
                    break;
                case "mariadb":
                    await backend.RunPowerShellInlineAsync(title, @"
. '" + System.IO.Path.Combine(backend.ScriptsDir, "common.ps1") + @"'
$settings = Ensure-ValidEnvForMachine
$rootPassword = $settings['MARIADB_ROOT_PASSWORD']
$mariaDir = Get-MariaDbDir
New-Item -ItemType Directory -Force -Path $mariaDir | Out-Null
if (-not (Test-Path ""$mariaDir\bin\mariadbd.exe"")) {
    $mariaZip = Join-Path $env:TEMP 'mariadb-11.4.zip'
    Invoke-WebRequest 'https://archive.mariadb.org/mariadb-11.4.8/winx64-packages/mariadb-11.4.8-winx64.zip' -OutFile $mariaZip -UseBasicParsing
    Expand-Archive $mariaZip $env:TEMP\mariadb-extract -Force
    $inner = Get-ChildItem ""$env:TEMP\mariadb-extract"" -Directory | Select-Object -First 1
    if ($inner) { Get-ChildItem $inner.FullName | Move-Item -Destination $mariaDir -Force }
    Remove-Item $mariaZip, ""$env:TEMP\mariadb-extract"" -Recurse -Force -ErrorAction SilentlyContinue
}
if (-not (Test-Path ""$mariaDir\data\mysql"")) {
    if (Test-Path ""$mariaDir\data"") { Remove-Item ""$mariaDir\data"" -Recurse -Force -ErrorAction SilentlyContinue }
    & ""$mariaDir\bin\mariadb-install-db.exe"" --datadir=""$mariaDir\data"" --password=""$rootPassword""
}
Optimize-HardwareConfig | Out-Null
if (-not (Get-Service -Name 'MariaDB' -ErrorAction SilentlyContinue)) {
    & ""$mariaDir\bin\mariadbd.exe"" --install MariaDB --defaults-file=""$mariaDir\data\my.ini""
} else {
    $expectedBin = ""`""$mariaDir\bin\mariadbd.exe`"" --defaults-file=`""$mariaDir\data\my.ini`"" MariaDB""
    & sc.exe config MariaDB binPath= $expectedBin | Out-Null
}
$svc = Get-Service -Name 'MariaDB' -ErrorAction SilentlyContinue
if ($svc -and $svc.Status -ne 'Running') { Start-Service MariaDB }
");
                    break;
                case "lfs":
                    await backend.RunPowerShellInlineAsync(title, "git lfs install --local\r\ngit lfs pull");
                    break;
                case "nginx":
                    await backend.RunPowerShellInlineAsync(title, @"
. '" + System.IO.Path.Combine(backend.ScriptsDir, "common.ps1") + @"'
$root = $script:ProjectRoot; $settings = Ensure-ValidEnvForMachine; $nginxDir = Get-NginxDir
New-Item -ItemType Directory -Force -Path $nginxDir | Out-Null
if (-not (Get-NginxExe)) {
    $zip = Join-Path $env:TEMP 'nginx.zip'
    Invoke-WebRequest 'https://nginx.org/download/nginx-1.27.5.zip' -OutFile $zip -UseBasicParsing
    Expand-Archive $zip ""$env:TEMP\nginx-extract"" -Force
    $inner = Get-ChildItem ""$env:TEMP\nginx-extract"" -Directory | Select-Object -First 1
    if ($inner) { Get-ChildItem $inner.FullName | Move-Item -Destination $nginxDir -Force }
    Remove-Item $zip, ""$env:TEMP\nginx-extract"" -Recurse -Force -ErrorAction SilentlyContinue
}
Ensure-ValidSslCertificate $settings
& (Join-Path $nginxDir 'nginx.exe') -t -p $nginxDir
");
                    break;
                case "patchserver":
                    await backend.RunPowerShellInlineAsync(title, @"
. '" + System.IO.Path.Combine(backend.ScriptsDir, "common.ps1") + @"'
$root = $script:ProjectRoot; $settings = Ensure-ValidEnvForMachine; $patchRoot = Get-PatchRoot $settings
New-Item -ItemType Directory -Force -Path ""$patchRoot\patch\files"", ""$patchRoot\patcher"" | Out-Null
foreach ($f in 'file_server.py','patch_watch.py') { Copy-Item (Join-Path $root ""source\patchserver\$f"") (Join-Path $patchRoot $f) -Force }
$patchCfgJson = @{ game_dir = (Join-Path $root 'runtime\client\game'); patch_dir = ""$patchRoot\patch""; patcher_dir = ""$patchRoot\patcher""; base_url = (Get-PublicBase $settings) } | ConvertTo-Json
Write-Utf8NoBom (Join-Path $patchRoot 'patchserver.json') $patchCfgJson
$cmd = Join-Path $root 'scripts\windows\start-stack.cmd'
$act = New-ScheduledTaskAction -Execute $cmd -WorkingDirectory (Join-Path $root 'scripts\windows')
$trg = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName 'VALIANT2-Stack' -Action $act -Trigger $trg -Force -Description 'VALIANT2 web/patch altyapisi' | Out-Null
$ports = 80,443,30001,30003,30005,30007,30009,30051
if (-not (Get-NetFirewallRule -DisplayName 'VALIANT2-Public' -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -DisplayName 'VALIANT2-Public' -Direction Inbound -Action Allow -Protocol TCP -LocalPort $ports | Out-Null
}
");
                    break;
                case "database":
                    await backend.RunPowerShellScriptAsync("Veritabanı Şema Kurulumu", "setup-database.ps1");
                    break;
                case "symlinks":
                    await backend.RunPowerShellScriptAsync("Config & Symlink Senkronizasyonu", "sync-config.ps1");
                    break;
                case "build":
                    await backend.RunPowerShellScriptAsync("Tüm Kaynakları Derle", "build-all.ps1");
                    break;
            }
        }
    }
}
