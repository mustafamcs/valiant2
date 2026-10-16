using System;
using System.Drawing;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Valiant2ControlCenter.Pages
{
    internal sealed class BuildPackPage : BufferedPanel
    {
        private readonly BackendService backend;
        private readonly DataGridView gridPacks;
        private readonly Label lblPacksHeader;

        public BuildPackPage(BackendService backend)
        {
            this.backend = backend;
            Dock = DockStyle.Fill;
            BackColor = Theme.BgMain;
            Padding = new Padding(8, 6, 8, 6);

            var split = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 2,
                RowCount = 1,
                BackColor = Color.Transparent
            };
            split.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 310F));
            split.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));

            // Left Card: C++ / C# Build Buttons
            var buildCard = new BufferedPanel
            {
                Dock = DockStyle.Fill,
                BackColor = Theme.BgCard,
                DrawCardBorder = true,
                Margin = new Padding(0, 0, 4, 0),
                Padding = new Padding(10)
            };

            var lblBuildTitle = new Label
            {
                Text = "KAYNAK DERLEME (" + backend.CpuThreads + " THREAD)",
                Font = Theme.FontCardTitle,
                ForeColor = Theme.GoldBright,
                Location = new Point(10, 8),
                AutoSize = true
            };

            int y = 30;
            AddFullWidthBtn(buildCard, "★ TÜMÜNÜ DERLE (KOD + PACK)", ButtonStyle.PrimaryCrimson, ref y, () =>
                backend.RunPowerShellScriptAsync("Tam Derleme (build-all.ps1)", "build-all.ps1"));

            AddFullWidthBtn(buildCard, "⚡ HIZLI DERLE (PACKSİZ)", ButtonStyle.PrimaryGold, ref y, () =>
                backend.RunPowerShellScriptAsync("Hızlı Derleme (-SkipPacks)", "build-all.ps1", "-SkipPacks"));

            AddFullWidthBtn(buildCard, "🛡 SADECE SERVER DERLE (game/db)", ButtonStyle.Secondary, ref y, () =>
                BuildSingleSolution("Server (AntrumServer.sln)", @"source\server\source\AntrumServer.sln", "Release", "Win32"));

            AddFullWidthBtn(buildCard, "⚔ SADECE CLIENT DERLE (M2Client)", ButtonStyle.Secondary, ref y, () =>
                BuildSingleSolution("Client (Antrum_Client_Global.sln)", @"source\client\Antrum_Client_Global.sln", "Release", "Win32"));

            AddFullWidthBtn(buildCard, "✦ AUTOPATCHER DERLE & DAĞIT", ButtonStyle.Success, ref y, () =>
                backend.RunPowerShellScriptAsync("Autopatcher Derle & Dağıt", "build-patcher.ps1"));

            AddFullWidthBtn(buildCard, "📜 QUESTLERİ DERLE & YÜKLE (qc.exe)", ButtonStyle.PrimaryGold, ref y, () =>
                backend.RunPowerShellScriptAsync("Quest Derleme (build-quests.ps1)", "build-quests.ps1"));

            var btnDump = Theme.CreateButton("⚙ CONFIG.EXE", ButtonStyle.Secondary, 92, 28);
            btnDump.Location = new Point(10, y);
            btnDump.Click += async (s, e) => await BuildSingleSolution("Client Config (config.exe)", @"tools\client-config\Valiant2Config.csproj", "Release", "AnyCPU");

            var btnVerify = Theme.CreateButton("DENETLE", ButtonStyle.Success, 94, 28);
            btnVerify.Location = new Point(107, y);
            btnVerify.Click += async (s, e) => await backend.RunPowerShellScriptAsync("Proje Bütünlük Denetimi", "verify-project.ps1");

            var btnClean = Theme.CreateButton("TEMİZLE", ButtonStyle.Danger, 91, 28);
            btnClean.Location = new Point(205, y);
            btnClean.Click += async (s, e) => await backend.RunPowerShellScriptAsync("Proje Temizliği", "cleanup-project.ps1");

            buildCard.Controls.AddRange(new Control[] { lblBuildTitle, btnDump, btnVerify, btnClean });

            // Right Card: Pack Studio
            var packCard = new BufferedPanel
            {
                Dock = DockStyle.Fill,
                BackColor = Theme.BgCard,
                DrawCardBorder = true,
                Margin = new Padding(4, 0, 0, 0),
                Padding = new Padding(10)
            };

            var packTop = new Panel { Dock = DockStyle.Top, Height = 56, BackColor = Color.Transparent };
            lblPacksHeader = new Label
            {
                Text = "FSARCHIVER PACK STÜDYOSU (Çift tıklayarak tek pack üretin)",
                Font = Theme.FontCardTitle,
                ForeColor = Theme.GoldBright,
                Location = new Point(2, 2),
                AutoSize = true
            };

            var packFlow = new FlowLayoutPanel
            {
                Location = new Point(0, 23),
                Size = new Size(470, 32),
                BackColor = Color.Transparent,
                WrapContents = false
            };

            AddMiniPackBtn(packFlow, "SEÇİLİ ÜRET", ButtonStyle.PrimaryCrimson, 96, async () =>
            {
                if (gridPacks.SelectedRows.Count == 0) return;
                string name = Convert.ToString(gridPacks.SelectedRows[0].Cells["Name"].Value);
                await BuildPackArchive(name);
            });
            AddMiniPackBtn(packFlow, "root", ButtonStyle.PrimaryGold, 66, () => BuildPackArchive("root"));
            AddMiniPackBtn(packFlow, "locale", ButtonStyle.PrimaryGold, 72, () => BuildPackArchive("locale"));
            AddMiniPackBtn(packFlow, "DEĞİŞENLER", ButtonStyle.Success, 102, async () =>
            {
                await backend.RunPowerShellScriptAsync("Değişen Packler Üretiliyor", "build-client-packs.ps1");
                RefreshPacks();
            });
            AddMiniPackBtn(packFlow, "TÜMÜ", ButtonStyle.Secondary, 62, async () =>
            {
                await backend.RunPowerShellScriptAsync("Tüm Packler Zorla Üretiliyor", "build-client-packs.ps1", "-Force");
                RefreshPacks();
            });
            AddMiniPackBtn(packFlow, "↻", ButtonStyle.Secondary, 34, () => { RefreshPacks(); return Task.CompletedTask; });

            packTop.Controls.AddRange(new Control[] { lblPacksHeader, packFlow });

            gridPacks = Theme.CreateGrid();
            gridPacks.Dock = DockStyle.Fill;
            gridPacks.Columns.Add("Name", "Pack");
            gridPacks.Columns.Add("PakFile", "Arşiv");
            gridPacks.Columns.Add("Size", "Boyut");
            gridPacks.Columns.Add("Modified", "Tarih");
            gridPacks.Columns.Add("Status", "Durum");
            gridPacks.Columns["Name"].FillWeight = 65;
            gridPacks.Columns["PakFile"].FillWeight = 75;
            gridPacks.Columns["Size"].FillWeight = 55;
            gridPacks.Columns["Status"].FillWeight = 55;
            gridPacks.CellDoubleClick += async (s, e) =>
            {
                if (e.RowIndex < 0) return;
                string name = Convert.ToString(gridPacks.Rows[e.RowIndex].Cells["Name"].Value);
                await BuildPackArchive(name);
            };

            packCard.Controls.Add(gridPacks);
            Theme.AttachGridScrollBar(gridPacks, packCard);
            packCard.Controls.Add(packTop);

            split.Controls.Add(buildCard, 0, 0);
            split.Controls.Add(packCard, 1, 0);
            Controls.Add(split);

            RefreshPacks();
        }

        private static void AddFullWidthBtn(Control parent, string text, ButtonStyle style, ref int y, Func<Task> action)
        {
            var btn = Theme.CreateButton(text, style, 286, 29);
            btn.Location = new Point(10, y);
            btn.Click += async (s, e) => await action();
            parent.Controls.Add(btn);
            y += 33;
        }

        private static void AddMiniPackBtn(FlowLayoutPanel flow, string text, ButtonStyle style, int width, Func<Task> action)
        {
            var btn = Theme.CreateButton(text, style, width, 26);
            btn.Margin = new Padding(0, 0, 4, 0);
            btn.Font = Theme.FontButtonSm;
            btn.Click += async (s, e) => await action();
            flow.Controls.Add(btn);
        }

        private async Task BuildSingleSolution(string title, string relSlnPath, string config, string platform)
        {
            int threads = backend.CpuThreads;
            bool isServer = relSlnPath.IndexOf("AntrumServer", StringComparison.OrdinalIgnoreCase) >= 0;
            string script = string.Format(@"
$sw = [Diagnostics.Stopwatch]::StartNew()
. '{0}'
$hw = Optimize-HardwareConfig
$threads = {5}
$vswhere = Join-Path ${{env:ProgramFiles(x86)}} 'Microsoft Visual Studio\Installer\vswhere.exe'
$msbuild = & $vswhere -latest -products * -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1
& '{1}'
$srvRunning = $false
if (${6}) {{
    $srvRunning = [bool](Get-Process -Name 'game','db' -ErrorAction SilentlyContinue)
    Write-Host 'Sunucu surecleri (game.exe + db.exe) derleme icin kapatiliyor...'
    Stop-ServerProcesses
}} else {{
    Write-Host 'Istemci surecleri (M2Client.exe / config.exe) derleme icin kapatiliyor...'
    Stop-ClientProcesses
}}
$env:CL = ""/MP$threads""
& $msbuild '{2}' /m:$threads /p:CL_MPCount=$threads /p:UseMultiToolTask=true /p:EnforceProcessCountAcrossBuilds=true /t:Build /p:Configuration={3} /p:Platform={4} /v:minimal /nologo
if ($LASTEXITCODE -ne 0) {{ throw ""Derleme hatasi: $LASTEXITCODE"" }}
if ($srvRunning) {{ & '{7}' }}
$sw.Stop()
Write-Host ""{8} $([math]::Round($sw.Elapsed.TotalSeconds, 2)) sn icinde derlendi.""
",
                System.IO.Path.Combine(backend.ScriptsDir, "common.ps1"),
                System.IO.Path.Combine(backend.ScriptsDir, "sync-config.ps1"),
                System.IO.Path.Combine(backend.ProjectRoot, relSlnPath),
                config, platform, threads, isServer ? "true" : "false",
                System.IO.Path.Combine(backend.ScriptsDir, "start-server.ps1"), title);

            await backend.RunPowerShellInlineAsync("Derleniyor: " + title, script);
        }

        private async Task BuildPackArchive(string packName)
        {
            await backend.RunPowerShellScriptAsync("Pack Üretiliyor: " + packName + ".pak", "build-client-packs.ps1", "-Archive \"" + packName + "\"");
            RefreshPacks();
        }

        public void RefreshPacks()
        {
            Task.Run(() =>
            {
                var packs = backend.GetPackEntries();
                if (IsDisposed) return;
                BeginInvoke(new Action(() =>
                {
                    gridPacks.Rows.Clear();
                    long totalBytes = 0;
                    int ready = 0;
                    foreach (var p in packs)
                    {
                        if (p.Exists) { ready++; totalBytes += p.SizeBytes; }
                        string sizeTxt = p.Exists ? (p.SizeBytes >= 1048576 ? (p.SizeBytes / 1048576.0).ToString("0.0") + " MB" : (p.SizeBytes / 1024.0).ToString("0") + " KB") : "-";
                        string dateTxt = p.Exists ? p.LastModified.ToString("HH:mm:ss") : "-";
                        gridPacks.Rows.Add(p.Name, p.PakFile, sizeTxt, dateTxt, p.Exists ? "Hazır" : "Eksik");
                    }
                    lblPacksHeader.Text = string.Format("PACK STÜDYOSU ({0}/{1} Hazır • {2:0.0} MB • Çift tıkla üret)", ready, packs.Count, totalBytes / 1048576.0);
                }));
            });
        }
    }
}
