using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

namespace Valiant2ControlCenter.Pages
{
    internal sealed class DashboardPage : BufferedPanel
    {
        private readonly BackendService backend;
        private readonly Action<int> navigateToPage;

        private readonly MiniServicePill pillMaria;
        private readonly MiniServicePill pillDbPeer;
        private readonly MiniServicePill pillAuth;
        private readonly MiniServicePill pillCh1C1;
        private readonly MiniServicePill pillCh1C2;
        private readonly MiniServicePill pillCh1C3;
        private readonly MiniServicePill pillCh1C4;
        private readonly MiniServicePill pillCh99;
        private readonly MiniServicePill pillNginx;
        private readonly MiniServicePill pillPhp;
        private readonly MiniServicePill pillPatchSrv;
        private readonly MiniServicePill pillWatcher;

        private readonly Label lblInfoLine;

        public DashboardPage(BackendService backend, Action<int> navigateToPage)
        {
            this.backend = backend;
            this.navigateToPage = navigateToPage;
            Dock = DockStyle.Fill;
            BackColor = Theme.BgMain;
            Padding = new Padding(8, 6, 8, 6);

            // 1. Compact Status Strip Card (Height = 84)
            var statusCard = new BufferedPanel
            {
                Dock = DockStyle.Top,
                Height = 86,
                BackColor = Theme.BgCard,
                DrawCardBorder = true,
                Padding = new Padding(8, 5, 8, 5)
            };

            lblInfoLine = new Label
            {
                Text = "CANLI SERVİSLER  •  Kontrol ediliyor...",
                Font = Theme.FontCardTitle,
                ForeColor = Theme.GoldBright,
                Location = new Point(8, 5),
                Size = new Size(780, 18),
                UseMnemonic = false
            };

            var pillFlow = new FlowLayoutPanel
            {
                Location = new Point(6, 25),
                Size = new Size(784, 56),
                BackColor = Color.Transparent,
                WrapContents = true
            };

            pillMaria    = new MiniServicePill("MariaDB (3306)");
            pillDbPeer   = new MiniServicePill("DB Peer (30000)");
            pillAuth     = new MiniServicePill("Auth (30001)");
            pillCh1C1    = new MiniServicePill("CH1 Core 1");
            pillCh1C2    = new MiniServicePill("CH1 Core 2");
            pillCh1C3    = new MiniServicePill("CH1 Core 3");
            pillCh1C4    = new MiniServicePill("CH1 Core 4");
            pillCh99     = new MiniServicePill("CH99 Ortak");
            pillNginx    = new MiniServicePill("Nginx (443)");
            pillPhp      = new MiniServicePill("PHP Panel (x4)");
            pillPatchSrv = new MiniServicePill("Patch Sunucu");
            pillWatcher  = new MiniServicePill("Patch İzleyici");

            pillFlow.Controls.AddRange(new Control[]
            {
                pillMaria, pillDbPeer, pillAuth, pillCh1C1, pillCh1C2, pillCh1C3,
                pillCh1C4, pillCh99, pillNginx, pillPhp, pillPatchSrv, pillWatcher
            });
            statusCard.Controls.AddRange(new Control[] { lblInfoLine, pillFlow });

            // 2. Three Compact Action Columns (Height = 158)
            var midTable = new TableLayoutPanel
            {
                Dock = DockStyle.Top,
                Height = 162,
                ColumnCount = 3,
                RowCount = 1,
                BackColor = Color.Transparent,
                Padding = new Padding(0, 6, 0, 6)
            };
            midTable.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33.33F));
            midTable.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33.33F));
            midTable.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33.34F));

            // Col 1: Game Server
            var colGame = CreateGroupCard("🛡 OYUN SUNUCUSU", new Padding(0, 0, 4, 0));
            var btnGameStart = Theme.CreateButton("▶ SUNUCUYU BAŞLAT", ButtonStyle.Success, 240, 30);
            btnGameStart.Location = new Point(10, 28);
            btnGameStart.Click += async (s, e) => await backend.RunPowerShellScriptAsync("Oyun Sunucusu Başlatılıyor", "start-server.ps1");

            var btnGameRestart = Theme.CreateButton("↻ RESTART", ButtonStyle.PrimaryCrimson, 117, 28);
            btnGameRestart.Location = new Point(10, 62);
            btnGameRestart.Click += async (s, e) =>
            {
                await backend.RunPowerShellScriptAsync("Oyun Sunucusu Durduruluyor", "stop-server.ps1");
                await backend.RunPowerShellScriptAsync("Oyun Sunucusu Başlatılıyor", "start-server.ps1");
            };

            var btnGameStop = Theme.CreateButton("■ DURDUR", ButtonStyle.Danger, 117, 28);
            btnGameStop.Location = new Point(133, 62);
            btnGameStop.Click += async (s, e) => await backend.RunPowerShellScriptAsync("Oyun Sunucusu Durduruluyor", "stop-server.ps1");

            var btnGameMin = Theme.CreateButton("⚡ TEK CORE", ButtonStyle.Secondary, 117, 28);
            btnGameMin.Location = new Point(10, 94);
            btnGameMin.Click += async (s, e) => await backend.RunPowerShellScriptAsync("Minimal Sunucu Başlatılıyor", "start-server.ps1", "-Minimal");

            var btnSyncCfg = Theme.CreateButton("⚙ CONFIG", ButtonStyle.Secondary, 117, 28);
            btnSyncCfg.Location = new Point(133, 94);
            btnSyncCfg.Click += async (s, e) => await backend.RunPowerShellScriptAsync("Config & IP Senkronizasyonu", "sync-config.ps1");

            colGame.Controls.AddRange(new Control[] { btnGameStart, btnGameRestart, btnGameStop, btnGameMin, btnSyncCfg });

            // Col 2: Web & Patch Stack
            var colStack = CreateGroupCard("🌐 WEB & PATCH STACK", new Padding(2, 0, 2, 0));
            var btnStackStart = Theme.CreateButton("▶ STACK BAŞLAT", ButtonStyle.PrimaryGold, 240, 30);
            btnStackStart.Location = new Point(10, 28);
            btnStackStart.Click += async (s, e) => await backend.RunPowerShellScriptAsync("Web & Patch Stack Başlatılıyor", "start-stack.ps1");

            var btnStackRestart = Theme.CreateButton("↻ RESTART", ButtonStyle.Secondary, 117, 28);
            btnStackRestart.Location = new Point(10, 62);
            btnStackRestart.Click += async (s, e) =>
            {
                await backend.RunPowerShellScriptAsync("Stack Durduruluyor", "stop-stack.ps1");
                await backend.RunPowerShellScriptAsync("Stack Başlatılıyor", "start-stack.ps1");
            };

            var btnStackStop = Theme.CreateButton("■ DURDUR", ButtonStyle.Danger, 117, 28);
            btnStackStop.Location = new Point(133, 62);
            btnStackStop.Click += async (s, e) => await backend.RunPowerShellScriptAsync("Web & Patch Stack Durduruluyor", "stop-stack.ps1");

            var btnManifest = Theme.CreateButton("📦 MANIFEST", ButtonStyle.Secondary, 117, 28);
            btnManifest.Location = new Point(10, 94);
            btnManifest.Click += async (s, e) => await backend.RunPowerShellScriptAsync("Patch Manifest Yayınlanıyor", "publish-patch.ps1");

            var btnSsl = Theme.CreateButton("🔐 SSL YENİLE", ButtonStyle.Secondary, 117, 28);
            btnSsl.Location = new Point(133, 94);
            btnSsl.Click += async (s, e) => await backend.RunPowerShellScriptAsync("SSL Sertifikası Yenileniyor", "renew-cert.ps1");

            colStack.Controls.AddRange(new Control[] { btnStackStart, btnStackRestart, btnStackStop, btnManifest, btnSsl });

            // Col 3: Client & Tools
            var colClient = CreateGroupCard("⚔ OYUN & ARAÇLAR", new Padding(4, 0, 0, 0));
            var btnPlay = Theme.CreateButton("⚔ OYUNU BAŞLAT (M2Client)", ButtonStyle.PrimaryCrimson, 240, 30);
            btnPlay.Location = new Point(10, 28);
            btnPlay.Click += (s, e) => LaunchExe(@"runtime\client\game\bin\M2Client.exe", @"runtime\client\game");

            var btnPatcher = Theme.CreateButton("✦ PATCHER", ButtonStyle.Secondary, 117, 28);
            btnPatcher.Location = new Point(10, 62);
            btnPatcher.Click += (s, e) => LaunchExe(@"runtime\client\VALIANT2.exe", @"runtime\client");

            var btnPanel = Theme.CreateButton("🌐 WEB PANEL", ButtonStyle.Secondary, 117, 28);
            btnPanel.Location = new Point(133, 62);
            btnPanel.Click += (s, e) =>
            {
                var snap = backend.GetHealthSnapshot();
                try { Process.Start("https://" + snap.PublicIp + "/"); } catch { }
            };

            var btnCfgExe = Theme.CreateButton("⚙ AYARLAR", ButtonStyle.Secondary, 117, 28);
            btnCfgExe.Location = new Point(10, 94);
            btnCfgExe.Click += (s, e) => LaunchExe(@"runtime\client\game\bin\config.exe", @"runtime\client\game");

            var btnFolder = Theme.CreateButton("📁 KLASÖR", ButtonStyle.Secondary, 117, 28);
            btnFolder.Location = new Point(133, 94);
            btnFolder.Click += (s, e) => { try { Process.Start("explorer.exe", backend.ProjectRoot); } catch { } };

            colClient.Controls.AddRange(new Control[] { btnPlay, btnPatcher, btnPanel, btnCfgExe, btnFolder });

            midTable.Controls.Add(colGame, 0, 0);
            midTable.Controls.Add(colStack, 1, 0);
            midTable.Controls.Add(colClient, 2, 0);

            // 3. Bottom Master Bar (Height = 44)
            var bottomBar = new BufferedPanel
            {
                Dock = DockStyle.Fill,
                BackColor = Theme.BgCard,
                DrawCardBorder = true,
                Padding = new Padding(8, 5, 8, 5)
            };

            var btnAllStart = Theme.CreateButton("★ TÜM SİSTEMİ BAŞLAT (OYUN + WEB + PATCH)", ButtonStyle.Success, 385, 32);
            btnAllStart.Location = new Point(8, 6);
            btnAllStart.Click += async (s, e) =>
            {
                await backend.RunPowerShellScriptAsync("Web & Patch Stack Başlatılıyor", "start-stack.ps1");
                await backend.RunPowerShellScriptAsync("Oyun Sunucusu Başlatılıyor", "start-server.ps1");
            };

            var btnAllStop = Theme.CreateButton("■ TÜM SİSTEMİ DURDUR", ButtonStyle.Danger, 235, 32);
            btnAllStop.Location = new Point(401, 6);
            btnAllStop.Click += async (s, e) =>
            {
                await backend.RunPowerShellScriptAsync("Oyun Sunucusu Durduruluyor", "stop-server.ps1");
                await backend.RunPowerShellScriptAsync("Web & Patch Stack Durduruluyor", "stop-stack.ps1");
            };

            var btnGoSetup = Theme.CreateButton("★ KURULUM", ButtonStyle.PrimaryGold, 148, 32);
            btnGoSetup.Location = new Point(644, 6);
            btnGoSetup.Click += (s, e) => this.navigateToPage(2);

            bottomBar.Controls.AddRange(new Control[] { btnAllStart, btnAllStop, btnGoSetup });

            Controls.Add(bottomBar);
            Controls.Add(midTable);
            Controls.Add(statusCard);
        }

        private static BufferedPanel CreateGroupCard(string title, Padding margin)
        {
            var card = new BufferedPanel
            {
                Dock = DockStyle.Fill,
                Margin = margin,
                BackColor = Theme.BgCard,
                DrawCardBorder = true
            };
            var lbl = new Label
            {
                Text = title,
                Font = Theme.FontCardTitle,
                ForeColor = Theme.GoldBright,
                Location = new Point(10, 7),
                AutoSize = true,
                UseMnemonic = false
            };
            card.Controls.Add(lbl);
            return card;
        }

        private void LaunchExe(string relExe, string relWorkDir)
        {
            string exePath = Path.Combine(backend.ProjectRoot, relExe);
            string workDir = Path.Combine(backend.ProjectRoot, relWorkDir);
            if (!File.Exists(exePath))
            {
                MessageBox.Show("Dosya bulunamadı:\n" + exePath, "VALIANT2", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }
            try { Process.Start(new ProcessStartInfo { FileName = exePath, WorkingDirectory = workDir, UseShellExecute = true }); }
            catch (Exception ex) { MessageBox.Show("Hata: " + ex.Message); }
        }

        public void ApplySnapshot(ServiceHealthSnapshot s)
        {
            if (IsDisposed) return;

            lblInfoLine.Text = string.Format(
                "CANLI DURUM  •  Oyun: {0}/7 Core  •  Web/Patch: {1}  •  Hesap: {2} (GM: {3})  •  IP: {4}  •  Ver: {5} (Patch v{6})",
                s.RunningGameCoresCount,
                s.WebStackHealthy ? "AÇIK" : "KAPALI",
                s.AccountCount, s.GmCount, s.PublicIp, s.ClientVersion, s.PatchVersion);

            pillMaria.UpdateState(s.MariaDbRunning);
            pillDbPeer.UpdateState(s.DbPeerOpen);
            pillAuth.UpdateState(s.AuthOpen);
            pillCh1C1.UpdateState(s.Ch1Core1Open);
            pillCh1C2.UpdateState(s.Ch1Core2Open);
            pillCh1C3.UpdateState(s.Ch1Core3Open);
            pillCh1C4.UpdateState(s.Ch1Core4Open);
            pillCh99.UpdateState(s.Ch99Open);
            pillNginx.UpdateState(s.NginxRunning);
            pillPhp.UpdateState(s.PhpWorkerCount == 4, s.PhpWorkerCount > 0 && s.PhpWorkerCount < 4);
            pillPatchSrv.UpdateState(s.PatchFileServerOpen);
            pillWatcher.UpdateState(s.PatchWatcherRunning);
        }
    }
}
