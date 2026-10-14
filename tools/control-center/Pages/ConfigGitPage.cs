using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Valiant2ControlCenter.Pages
{
    internal sealed class ConfigGitPage : BufferedPanel
    {
        private readonly BackendService backend;
        private readonly TextBox txtPublicIp;
        private readonly TextBox txtServerName;
        private readonly TextBox txtCommitMsg;
        private readonly RichTextBox txtDiagOutput;

        public ConfigGitPage(BackendService backend)
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
            split.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 315F));
            split.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));

            // Left Card: Network / .env + Git Controls
            var leftCard = new BufferedPanel
            {
                Dock = DockStyle.Fill,
                BackColor = Theme.BgCard,
                DrawCardBorder = true,
                Margin = new Padding(0, 0, 4, 0),
                Padding = new Padding(10)
            };

            var lblNet = new Label { Text = "⚙ AĞ & .ENV YAPILANDIRMASI", Font = Theme.FontCardTitle, ForeColor = Theme.GoldBright, Location = new Point(10, 8), AutoSize = true };

            leftCard.Controls.Add(new Label { Text = "Sunucu IP:", Location = new Point(10, 32), AutoSize = true, Font = Theme.FontSmall, ForeColor = Theme.TextMain });
            txtPublicIp = Theme.CreateTextBox("");
            txtPublicIp.Location = new Point(82, 29);
            txtPublicIp.Size = new Size(212, 22);

            leftCard.Controls.Add(new Label { Text = "Sunucu Adı:", Location = new Point(10, 58), AutoSize = true, Font = Theme.FontSmall, ForeColor = Theme.TextMain });
            txtServerName = Theme.CreateTextBox("VALIANT2");
            txtServerName.Location = new Point(82, 55);
            txtServerName.Size = new Size(212, 22);

            var btnAutoIp = Theme.CreateButton("★ OTOMATİK IP", ButtonStyle.PrimaryGold, 102, 26);
            btnAutoIp.Location = new Point(10, 83);
            btnAutoIp.Font = Theme.FontButtonSm;
            btnAutoIp.Click += (s, e) => { txtPublicIp.Text = backend.DetectPublicIp(); };

            var btnLanIp = Theme.CreateButton("LAN IP", ButtonStyle.Secondary, 86, 26);
            btnLanIp.Location = new Point(116, 83);
            btnLanIp.Font = Theme.FontButtonSm;
            btnLanIp.Click += (s, e) =>
            {
                var lans = BackendService.GetLocalAdapterIps();
                txtPublicIp.Text = lans.Count > 0 ? lans[0] : "127.0.0.1";
            };

            var btnLocalIp = Theme.CreateButton("127.0.0.1", ButtonStyle.Secondary, 88, 26);
            btnLocalIp.Location = new Point(206, 83);
            btnLocalIp.Font = Theme.FontButtonSm;
            btnLocalIp.Click += (s, e) => { txtPublicIp.Text = "127.0.0.1"; };

            var btnSaveEnv = Theme.CreateButton("✓ .ENV KAYDET & TÜMÜNE UYGULA", ButtonStyle.PrimaryCrimson, 284, 29);
            btnSaveEnv.Location = new Point(10, 113);
            btnSaveEnv.Click += async (s, e) => await SaveAndSyncEnvAsync();

            // Git Section inside Left Card
            var lblGit = new Label { Text = "★ GİT DEPO & GITHUB PUSH", Font = Theme.FontCardTitle, ForeColor = Theme.GoldBright, Location = new Point(10, 152), AutoSize = true };

            txtCommitMsg = Theme.CreateTextBox("Update VALIANT2 changes");
            txtCommitMsg.Location = new Point(10, 174);
            txtCommitMsg.Size = new Size(284, 22);

            var btnGitPush = Theme.CreateButton("▶ COMMİTLE & PUSHLA", ButtonStyle.PrimaryCrimson, 182, 28);
            btnGitPush.Location = new Point(10, 202);
            btnGitPush.Click += async (s, e) =>
            {
                string msg = txtCommitMsg.Text.Trim();
                if (string.IsNullOrEmpty(msg)) msg = "Save changes";
                await backend.RunPowerShellScriptAsync("Git Kaydet", "git-save.ps1", "\"" + msg.Replace("\"", "'") + "\"");
                await backend.RunPowerShellScriptAsync("Git Push", "git-sync.ps1");
                ShowGitStatus();
            };

            var btnGitStatus = Theme.CreateButton("↻ DURUM", ButtonStyle.Secondary, 96, 28);
            btnGitStatus.Location = new Point(198, 202);
            btnGitStatus.Font = Theme.FontButtonSm;
            btnGitStatus.Click += (s, e) => ShowGitStatus();

            // Syserr & Process Quick Buttons at bottom of Left Card
            var lblDiag = new Label { Text = "♦ HATA (SYSERR) & SÜREÇ TANILAMA", Font = Theme.FontCardTitle, ForeColor = Theme.GoldBright, Location = new Point(10, 240), AutoSize = true };

            var btnScanSyserr = Theme.CreateButton("▶ SYSERR TARA", ButtonStyle.PrimaryGold, 138, 28);
            btnScanSyserr.Location = new Point(10, 262);
            btnScanSyserr.Click += (s, e) => ScanAllSyserrs();

            var btnClearSyserr = Theme.CreateButton("✕ LOG SIFIRLA", ButtonStyle.Danger, 140, 28);
            btnClearSyserr.Location = new Point(154, 262);
            btnClearSyserr.Click += (s, e) => ClearAllSyserrs();

            var btnShowProcs = Theme.CreateButton("🛡 ÇALIŞAN SÜREÇLERİ & RAM LİSTELE", ButtonStyle.Secondary, 284, 26);
            btnShowProcs.Location = new Point(10, 294);
            btnShowProcs.Click += (s, e) => ShowProcesses();

            leftCard.Controls.AddRange(new Control[]
            {
                lblNet, txtPublicIp, txtServerName, btnAutoIp, btnLanIp, btnLocalIp, btnSaveEnv,
                lblGit, txtCommitMsg, btnGitPush, btnGitStatus,
                lblDiag, btnScanSyserr, btnClearSyserr, btnShowProcs
            });

            // Right Card: Unified Output Viewer (Git Status / Syserr / Process Monitor)
            var rightCard = new BufferedPanel
            {
                Dock = DockStyle.Fill,
                BackColor = Theme.BgCard,
                DrawCardBorder = true,
                Margin = new Padding(4, 0, 0, 0),
                Padding = new Padding(8)
            };

            var lblOutTitle = new Label
            {
                Text = "DURUM / SYSERR / GİT / SÜREÇ İZLEYİCİ",
                Dock = DockStyle.Top,
                Height = 20,
                Font = Theme.FontCardTitle,
                ForeColor = Theme.GoldBright
            };

            txtDiagOutput = new RichTextBox
            {
                Dock = DockStyle.Fill,
                Multiline = true,
                ReadOnly = true,
                ScrollBars = RichTextBoxScrollBars.None,
                BackColor = Theme.BgConsole,
                ForeColor = Theme.TextMain,
                BorderStyle = BorderStyle.None,
                Font = Theme.FontMono,
                WordWrap = false
            };

            rightCard.Controls.Add(txtDiagOutput);
            Theme.AttachRichTextScrollBar(txtDiagOutput, rightCard);
            rightCard.Controls.Add(lblOutTitle);

            split.Controls.Add(leftCard, 0, 0);
            split.Controls.Add(rightCard, 1, 0);
            Controls.Add(split);

            LoadEnvIntoForm();
            ScanAllSyserrs();
        }

        public void LoadEnvIntoForm()
        {
            var env = backend.LoadEnv();
            txtPublicIp.Text = env.ContainsKey("PUBLIC_IP") ? env["PUBLIC_IP"] : backend.DetectPublicIp();
            txtServerName.Text = env.ContainsKey("CLIENT_SERVER_NAME") ? env["CLIENT_SERVER_NAME"] : "VALIANT2";
        }

        private async Task SaveAndSyncEnvAsync()
        {
            var dict = backend.LoadEnv();
            string ip = txtPublicIp.Text.Trim();
            if (string.IsNullOrEmpty(ip)) ip = backend.DetectPublicIp();
            dict["PUBLIC_IP"] = ip;
            dict["CLIENT_SERVER_IP"] = ip;
            dict["PANEL_BASE_URL"] = "https://" + ip + "/";
            dict["CLIENT_SERVER_NAME"] = txtServerName.Text.Trim();
            dict["PATCH_ROOT"] = Path.Combine(backend.ProjectRoot, @"runtime\patchserver");

            backend.SaveEnv(dict);
            await backend.RunPowerShellScriptAsync("Config & IP Senkronizasyonu", "sync-config.ps1");
            await backend.RunPowerShellScriptAsync("root.pak Paketleniyor", "build-client-packs.ps1", "-Archive \"root\"");
            await backend.RunPowerShellScriptAsync("Autopatcher Derleniyor", "build-patcher.ps1");
        }

        public void RefreshGitStatus()
        {
            LoadEnvIntoForm();
            ShowGitStatus();
        }

        private void ShowGitStatus()
        {
            Task.Run(() =>
            {
                try
                {
                    var psi = new System.Diagnostics.ProcessStartInfo
                    {
                        FileName = "cmd.exe",
                        Arguments = "/c git status --short --branch && echo. && echo --- SON 8 COMMIT --- && git log -n 8 --oneline",
                        WorkingDirectory = backend.ProjectRoot,
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        CreateNoWindow = true,
                        StandardOutputEncoding = Encoding.UTF8
                    };
                    using (var p = System.Diagnostics.Process.Start(psi))
                    {
                        string output = p.StandardOutput.ReadToEnd() + p.StandardError.ReadToEnd();
                        p.WaitForExit(4000);
                        string norm = System.Text.RegularExpressions.Regex.Replace(output.Trim(), @"\r?\n", "\r\n");
                        if (!IsDisposed) BeginInvoke(new Action(() => txtDiagOutput.Text = norm));
                    }
                }
                catch { }
            });
        }

        private void ShowProcesses()
        {
            var procs = backend.GetManagedProcesses();
            var sb = new StringBuilder();
            sb.AppendLine("=== ÇALIŞAN SUNUCU VE ALTYAPI SÜREÇLERİ ===");
            double totalMb = 0;
            foreach (var p in procs)
            {
                totalMb += p.MemoryMb;
                sb.AppendLine(string.Format("{0,-22} | PID: {1,-6} | {2,6:0.0} MB | {3}", p.Role, p.Pid, p.MemoryMb, p.Status));
            }
            sb.AppendLine("-------------------------------------------");
            sb.AppendLine(string.Format("Toplam Bellek Kullanımı: {0:0.0} MB", totalMb));
            txtDiagOutput.Text = sb.ToString();
        }

        private void ScanAllSyserrs()
        {
            var sb = new StringBuilder();
            sb.AppendLine("=== SYSERR HATA TARAMASI (" + DateTime.Now.ToString("HH:mm:ss") + ") ===");
            string srvRoot = Path.Combine(backend.ProjectRoot, @"runtime\server\main\srv1");
            string[] cores = { "db", "auth", @"chan\ch1\core1", @"chan\ch1\core2", @"chan\ch1\core3", @"chan\ch1\core4", @"chan\ch99\core99" };

            int errCount = 0;
            foreach (var c in cores)
            {
                string f = Path.Combine(srvRoot, c, "syserr.txt");
                if (!File.Exists(f)) f = Path.Combine(srvRoot, c, "syserr");
                long len = File.Exists(f) ? new FileInfo(f).Length : 0;
                sb.AppendLine(string.Format("• {0,-16} : {1}", c.Replace(@"chan\", ""), len == 0 ? "TEMİZ (0 B)" : (len + " B")));
                if (len > 0) errCount++;
            }
            string cliSyserr = Path.Combine(backend.ProjectRoot, @"runtime\client\game\syserr.txt");
            long cliLen = File.Exists(cliSyserr) ? new FileInfo(cliSyserr).Length : 0;
            sb.AppendLine(string.Format("• {0,-16} : {1}", "client/syserr", cliLen == 0 ? "TEMİZ (0 B)" : (cliLen + " B")));
            txtDiagOutput.Text = sb.ToString();
        }

        private void ClearAllSyserrs()
        {
            string srvRoot = Path.Combine(backend.ProjectRoot, @"runtime\server\main\srv1");
            string[] cores = { "db", "auth", @"chan\ch1\core1", @"chan\ch1\core2", @"chan\ch1\core3", @"chan\ch1\core4", @"chan\ch99\core99" };
            foreach (var c in cores)
            {
                foreach (var n in new[] { "syserr.txt", "syserr" })
                {
                    string f = Path.Combine(srvRoot, c, n);
                    if (File.Exists(f))
                    {
                        try { using (var fs = new FileStream(f, FileMode.Truncate, FileAccess.Write, FileShare.ReadWrite)) { } } catch { }
                    }
                }
            }
            ScanAllSyserrs();
        }
    }
}
