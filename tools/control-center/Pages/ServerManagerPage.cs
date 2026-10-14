using System;
using System.Diagnostics;
using System.Drawing;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Valiant2ControlCenter.Pages
{
    internal sealed class ServerManagerPage : BufferedPanel
    {
        private readonly BackendService backend;
        private readonly DataGridView gridProcs;
        private readonly Label lblProcSummary;

        public ServerManagerPage(BackendService backend)
        {
            this.backend = backend;
            Dock = DockStyle.Fill;
            BackColor = Theme.BgMain;
            Padding = new Padding(14);

            var topContainer = new TableLayoutPanel
            {
                Dock = DockStyle.Top,
                Height = 178,
                ColumnCount = 2,
                RowCount = 1,
                BackColor = Color.Transparent,
                Padding = new Padding(0, 0, 0, 10)
            };
            topContainer.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            topContainer.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));

            var gameCard = new BufferedPanel { Dock = DockStyle.Fill, BackColor = Theme.BgCard, DrawCardBorder = true, Margin = new Padding(0, 0, 6, 0), Padding = new Padding(12) };
            var lblGameTitle = new Label { Text = "OYUN SUNUCUSU YÖNETİMİ (DB / AUTH / CH1 / CH99)", Font = Theme.FontCardTitle, ForeColor = Theme.GoldBright, AutoSize = true, Location = new Point(12, 10), UseMnemonic = false };
            var lblGameSub = new Label { Text = "MariaDB kontrolü, CONFIG senkronizasyonu ve core süreçlerini yönetir.", Font = Theme.FontSmall, ForeColor = Theme.TextMuted, AutoSize = true, Location = new Point(12, 30), UseMnemonic = false };

            var gameFlow = new FlowLayoutPanel { Location = new Point(12, 54), Size = new Size(455, 104), BackColor = Color.Transparent };
            AddCmdBtn(gameFlow, "▶ TAM BAŞLAT (TÜMÜ)", ButtonStyle.Success, 210, () => backend.RunPowerShellScriptAsync("Oyun Sunucusu Başlatılıyor", "start-server.ps1"));
            AddCmdBtn(gameFlow, "▶ MİNİMAL BAŞLAT (TEK)", ButtonStyle.PrimaryGold, 210, () => backend.RunPowerShellScriptAsync("Minimal Oyun Sunucusu Başlatılıyor", "start-server.ps1", "-Minimal"));
            AddCmdBtn(gameFlow, "■ SUNUCUYU DURDUR", ButtonStyle.Danger, 210, () => backend.RunPowerShellScriptAsync("Oyun Sunucusu Durduruluyor", "stop-server.ps1"));
            AddCmdBtn(gameFlow, "↻ YENİDEN BAŞLAT", ButtonStyle.PrimaryCrimson, 210, async () =>
            {
                await backend.RunPowerShellScriptAsync("Oyun Sunucusu Durduruluyor", "stop-server.ps1");
                await backend.RunPowerShellScriptAsync("Oyun Sunucusu Başlatılıyor", "start-server.ps1");
            });
            AddCmdBtn(gameFlow, "⚙ CONFIG SENKRONİZE ET", ButtonStyle.Secondary, 210, () => backend.RunPowerShellScriptAsync("Config Senkronize Ediliyor", "sync-config.ps1"));
            AddCmdBtn(gameFlow, "🔒 CONFIG KORUMASI", ButtonStyle.Secondary, 210, () => backend.RunPowerShellScriptAsync("Config Placeholder Koruması", "protect-config.ps1"));
            gameCard.Controls.AddRange(new Control[] { lblGameTitle, lblGameSub, gameFlow });

            var stackCard = new BufferedPanel { Dock = DockStyle.Fill, BackColor = Theme.BgCard, DrawCardBorder = true, Margin = new Padding(6, 0, 0, 0), Padding = new Padding(12) };
            var lblStackTitle = new Label { Text = "WEB PANEL & AUTOPATCHER ALTYAPISI (STACK)", Font = Theme.FontCardTitle, ForeColor = Theme.GoldBright, AutoSize = true, Location = new Point(12, 10), UseMnemonic = false };
            var lblStackSub = new Label { Text = "Nginx (443/80), 4x PHP Worker, Patch Dosya Sunucusu (8091) ve Watcher.", Font = Theme.FontSmall, ForeColor = Theme.TextMuted, AutoSize = true, Location = new Point(12, 30), UseMnemonic = false };

            var stackFlow = new FlowLayoutPanel { Location = new Point(12, 54), Size = new Size(455, 104), BackColor = Color.Transparent };
            AddCmdBtn(stackFlow, "▶ STACK BAŞLAT", ButtonStyle.Success, 210, () => backend.RunPowerShellScriptAsync("Web & Patch Stack Başlatılıyor", "start-stack.ps1"));
            AddCmdBtn(stackFlow, "■ STACK DURDUR", ButtonStyle.Danger, 210, () => backend.RunPowerShellScriptAsync("Web & Patch Stack Durduruluyor", "stop-stack.ps1"));
            AddCmdBtn(stackFlow, "↻ STACK YENİDEN BAŞLAT", ButtonStyle.PrimaryCrimson, 210, async () =>
            {
                await backend.RunPowerShellScriptAsync("Stack Durduruluyor", "stop-stack.ps1");
                await backend.RunPowerShellScriptAsync("Stack Başlatılıyor", "start-stack.ps1");
            });
            AddCmdBtn(stackFlow, "📦 MANIFEST YAYINLA (+1)", ButtonStyle.PrimaryGold, 210, () => backend.RunPowerShellScriptAsync("Patch Manifest Yayınlanıyor", "publish-patch.ps1"));
            AddCmdBtn(stackFlow, "🔐 SSL SERTİFİKASI YENİLE", ButtonStyle.Secondary, 210, () => backend.RunPowerShellScriptAsync("SSL Sertifikası Yenileniyor", "renew-cert.ps1"));
            AddCmdBtn(stackFlow, "📊 DETAYLI STACK TESTİ", ButtonStyle.Secondary, 210, () => backend.RunPowerShellScriptAsync("Stack Sağlık Kontrolü", "stack-status.ps1"));
            stackCard.Controls.AddRange(new Control[] { lblStackTitle, lblStackSub, stackFlow });

            topContainer.Controls.Add(gameCard, 0, 0);
            topContainer.Controls.Add(stackCard, 1, 0);

            var procCard = new BufferedPanel
            {
                Dock = DockStyle.Fill,
                BackColor = Theme.BgCard,
                DrawCardBorder = true,
                Padding = new Padding(12)
            };

            var procTopBar = new Panel { Dock = DockStyle.Top, Height = 38, BackColor = Color.Transparent };
            lblProcSummary = new Label
            {
                Text = "ÇALIŞAN SUNUCU VE ALTYAPI SÜREÇLERİ (PROCESS MONITOR)",
                Font = Theme.FontCardTitle,
                ForeColor = Theme.GoldBright,
                AutoSize = true,
                Location = new Point(2, 8),
                UseMnemonic = false
            };

            var btnKillSelected = Theme.CreateButton("SEÇİLİ SÜRECİ SONLANDIR", ButtonStyle.Danger, 195, 30);
            btnKillSelected.Font = new Font("Georgia", 8.25F, FontStyle.Bold);
            btnKillSelected.Click += (s, e) => KillSelectedProcess();

            var btnRefreshProcs = Theme.CreateButton("↻ LİSTEYİ YENİLE", ButtonStyle.Secondary, 140, 30);
            btnRefreshProcs.Font = new Font("Georgia", 8.25F, FontStyle.Bold);
            btnRefreshProcs.Click += (s, e) => RefreshProcessTable();

            procTopBar.Resize += (s, e) =>
            {
                btnRefreshProcs.Location = new Point(procTopBar.ClientSize.Width - btnRefreshProcs.Width - 2, 4);
                btnKillSelected.Location = new Point(btnRefreshProcs.Left - btnKillSelected.Width - 8, 4);
            };

            procTopBar.Controls.AddRange(new Control[] { lblProcSummary, btnKillSelected, btnRefreshProcs });

            gridProcs = Theme.CreateGrid();
            gridProcs.Dock = DockStyle.Fill;
            gridProcs.Columns.Add("Role", "Bileşen / Görev");
            gridProcs.Columns.Add("ProcessName", "Süreç Adı");
            gridProcs.Columns.Add("Pid", "PID");
            gridProcs.Columns.Add("MemoryMb", "RAM (MB)");
            gridProcs.Columns.Add("WorkingDir", "Kategori");
            gridProcs.Columns.Add("Status", "Durum");
            gridProcs.Columns["Pid"].FillWeight = 45;
            gridProcs.Columns["MemoryMb"].FillWeight = 55;
            gridProcs.Columns["Status"].FillWeight = 65;

            procCard.Controls.Add(gridProcs);
            procCard.Controls.Add(procTopBar);

            Controls.Add(procCard);
            Controls.Add(topContainer);

            RefreshProcessTable();
        }

        private static void AddCmdBtn(FlowLayoutPanel panel, string text, ButtonStyle style, int width, Func<Task> onClick)
        {
            var btn = Theme.CreateButton(text, style, width, 29);
            btn.Margin = new Padding(0, 0, 6, 5);
            btn.Font = new Font("Georgia", 8.0F, FontStyle.Bold);
            btn.Click += async (s, e) => await onClick();
            panel.Controls.Add(btn);
        }

        public void RefreshProcessTable()
        {
            Task.Run(() =>
            {
                var procs = backend.GetManagedProcesses();
                if (IsDisposed) return;
                BeginInvoke(new Action(() =>
                {
                    int selectedPid = -1;
                    if (gridProcs.SelectedRows.Count > 0 && gridProcs.SelectedRows[0].Cells["Pid"].Value != null)
                        int.TryParse(gridProcs.SelectedRows[0].Cells["Pid"].Value.ToString(), out selectedPid);

                    gridProcs.Rows.Clear();
                    double totalRam = 0;
                    int running = 0;
                    foreach (var p in procs)
                    {
                        totalRam += p.MemoryMb;
                        if (p.Status == "Çalışıyor") running++;
                        int idx = gridProcs.Rows.Add(p.Role, p.ProcessName, p.Pid, p.MemoryMb.ToString("0.0") + " MB", p.WorkingDir, p.Status);
                        if (p.Pid == selectedPid)
                            gridProcs.Rows[idx].Selected = true;
                    }
                    lblProcSummary.Text = string.Format("SUNUCU VE ALTYAPI SÜREÇLERİ ({0} Aktif — Toplam RAM: {1:0.0} MB)", running, totalRam);
                }));
            });
        }

        private void KillSelectedProcess()
        {
            if (gridProcs.SelectedRows.Count == 0) return;
            var row = gridProcs.SelectedRows[0];
            int pid = 0;
            int.TryParse(Convert.ToString(row.Cells["Pid"].Value), out pid);
            string role = Convert.ToString(row.Cells["Role"].Value);
            if (pid <= 0) return;

            if (MessageBox.Show(role + " (PID: " + pid + ") sürecini sonlandırmak istediğinize emin misiniz?",
                "Süreç Sonlandır", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) != DialogResult.Yes)
                return;

            try
            {
                var p = Process.GetProcessById(pid);
                p.Kill();
                backend.EmitLog(string.Format("Süreç sonlandırıldı: {0} (PID {1})", role, pid), false);
                RefreshProcessTable();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Süreç sonlandırılamadı: " + ex.Message, "Hata", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
