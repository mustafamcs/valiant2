using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Valiant2ControlCenter.Pages;

namespace Valiant2ControlCenter
{
    internal sealed class ControlCenterForm : Form
    {
        [DllImport("user32.dll")]
        private static extern bool ReleaseCapture();
        [DllImport("user32.dll")]
        private static extern IntPtr SendMessage(IntPtr hWnd, int msg, IntPtr wParam, IntPtr lParam);
        [DllImport("user32.dll")]
        private static extern bool PrintWindow(IntPtr hWnd, IntPtr hdcBlt, uint nFlags);

        private readonly BackendService backend;
        private readonly Image logoImg;
        private readonly List<TopTabButton> tabButtons = new List<TopTabButton>();
        private readonly List<Control> pages = new List<Control>();
        private readonly Panel contentHost;

        private readonly Label lblTopServerStatus;
        private readonly Label lblTaskBanner;
        private readonly Button btnStopTask;
        private readonly Panel consoleDrawer;
        private readonly RichTextBox rtbConsole;

        private readonly DashboardPage pageDashboard;
        private readonly BuildPackPage pageBuild;
        private readonly SetupWizardPage pageSetup;
        private readonly DatabaseGmPage pageDbGm;
        private readonly ConfigGitPage pageConfigGit;

        private readonly System.Windows.Forms.Timer healthTimer;
        private readonly System.Windows.Forms.Timer consoleFlushTimer;
        private readonly ConcurrentQueue<Tuple<string, bool>> consoleQueue = new ConcurrentQueue<Tuple<string, bool>>();
        private readonly object logFileLock = new object();
        private bool pollingHealth = false;
        private readonly string captureOutputDir;
        private readonly bool runE2eVerification;

        public ControlCenterForm(string captureOutputDir = null, bool runE2eVerification = false)
        {
            this.captureOutputDir = captureOutputDir;
            this.runE2eVerification = runE2eVerification;
            backend = new BackendService();

            Text = "VALIANT2 — Kontrol Paneli";
            AutoScaleMode = AutoScaleMode.None;
            StartPosition = FormStartPosition.CenterScreen;
            FormBorderStyle = FormBorderStyle.None;
            Size = new Size(820, 520);
            MinimumSize = new Size(820, 520);
            MaximumSize = new Size(820, 520);
            BackColor = Theme.BgDark;
            ForeColor = Theme.TextMain;
            Font = Theme.FontBody;
            DoubleBuffered = true;
            Padding = new Padding(2);

            try { Icon = Icon.ExtractAssociatedIcon(Application.ExecutablePath); } catch { }

            try
            {
                var asm = System.Reflection.Assembly.GetExecutingAssembly();
                var stream = asm.GetManifestResourceStream("logo.png");
                if (stream != null) logoImg = Image.FromStream(stream);
            }
            catch { }

            var topBar = CreateTopHeaderBar(out lblTopServerStatus);
            var tabStrip = CreateTopTabStrip();
            consoleDrawer = CreateConsoleDrawer(out rtbConsole, out lblTaskBanner, out btnStopTask);

            contentHost = new BufferedPanel
            {
                Dock = DockStyle.Fill,
                BackColor = Theme.BgMain
            };

            pageDashboard = new DashboardPage(backend, SelectPage);
            pageBuild     = new BuildPackPage(backend);
            pageSetup     = new SetupWizardPage(backend);
            pageDbGm      = new DatabaseGmPage(backend);
            pageConfigGit = new ConfigGitPage(backend);

            pages.AddRange(new Control[]
            {
                pageDashboard,
                pageBuild,
                pageSetup,
                pageDbGm,
                pageConfigGit
            });

            foreach (var p in pages)
            {
                p.Visible = false;
                contentHost.Controls.Add(p);
            }

            backend.OnOutputLine += AppendConsoleLine;
            backend.OnTaskStateChanged += UpdateTaskState;

            Controls.Add(contentHost);
            Controls.Add(consoleDrawer);
            Controls.Add(tabStrip);
            Controls.Add(topBar);

            Theme.DisableMnemonicsRecursive(this);
            SelectPage(0);

            AppendConsoleLine("VALIANT2 Hazır • Donanım: " + backend.HardwareSummary, false);

            consoleFlushTimer = new System.Windows.Forms.Timer { Interval = 90 };
            consoleFlushTimer.Tick += (s, e) => FlushConsoleQueue();
            consoleFlushTimer.Start();

            healthTimer = new System.Windows.Forms.Timer { Interval = 1500 };
            healthTimer.Tick += async (s, e) => await PollHealthAsync();
            healthTimer.Start();

            Shown += async (s, e) =>
            {
                await PollHealthAsync();
                if (this.runE2eVerification)
                    await RunFullE2eVerificationAndCaptureAsync(this.captureOutputDir);
                else if (!string.IsNullOrEmpty(this.captureOutputDir))
                    await CaptureAllPagesAndExitAsync(this.captureOutputDir);
            };
        }

        private Panel CreateTopHeaderBar(out Label statusLabel)
        {
            var bar = new BufferedPanel
            {
                Dock = DockStyle.Top,
                Height = 40,
                BackColor = Color.FromArgb(20, 15, 11)
            };
            bar.Paint += (s, e) =>
            {
                using (var br = new LinearGradientBrush(bar.ClientRectangle, Color.FromArgb(36, 26, 17), Color.FromArgb(16, 12, 9), LinearGradientMode.Vertical))
                    e.Graphics.FillRectangle(br, bar.ClientRectangle);
                if (logoImg != null)
                {
                    e.Graphics.InterpolationMode = InterpolationMode.HighQualityBicubic;
                    e.Graphics.DrawImage(logoImg, 10, 5, 86, 30);
                }
                using (var pen = new Pen(Theme.BorderGold, 1))
                    e.Graphics.DrawLine(pen, 0, bar.Height - 1, bar.Width, bar.Height - 1);
            };

            MouseEventHandler dragHandler = (s, e) =>
            {
                if (e.Button == MouseButtons.Left)
                {
                    ReleaseCapture();
                    SendMessage(Handle, 0xA1, new IntPtr(2), IntPtr.Zero);
                }
            };
            bar.MouseDown += dragHandler;

            var lblTitle = new Label
            {
                Text = "V A L I A N T  II  —  KONTROL MERKEZİ",
                Font = Theme.FontTitle,
                ForeColor = Theme.GoldBright,
                BackColor = Color.Transparent,
                AutoSize = true,
                Location = new Point(104, 10),
                UseMnemonic = false
            };
            lblTitle.MouseDown += dragHandler;

            var lblStatus = new Label
            {
                Name = "lblTopServerStatus",
                Text = "Kontrol ediliyor...",
                Font = Theme.FontBodyBold,
                ForeColor = Theme.GoldBright,
                BackColor = Color.FromArgb(28, 22, 15),
                BorderStyle = BorderStyle.FixedSingle,
                TextAlign = ContentAlignment.MiddleCenter,
                Size = new Size(295, 24),
                Location = new Point(442, 8),
                UseMnemonic = false
            };
            statusLabel = lblStatus;

            var btnMin = new Button
            {
                Text = "—",
                Size = new Size(28, 24),
                Location = new Point(746, 8),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(40, 32, 22),
                ForeColor = Theme.GoldBright,
                Cursor = Cursors.Hand
            };
            btnMin.FlatAppearance.BorderColor = Theme.BorderGold;
            btnMin.Click += (s, e) => WindowState = FormWindowState.Minimized;

            var btnClose = new Button
            {
                Text = "✕",
                Size = new Size(28, 24),
                Location = new Point(778, 8),
                FlatStyle = FlatStyle.Flat,
                BackColor = Theme.Crimson,
                ForeColor = Theme.GoldBright,
                Cursor = Cursors.Hand
            };
            btnClose.FlatAppearance.BorderColor = Theme.Gold;
            btnClose.Click += (s, e) => Close();

            bar.Controls.AddRange(new Control[] { lblTitle, lblStatus, btnMin, btnClose });
            return bar;
        }

        private Panel CreateTopTabStrip()
        {
            var strip = new BufferedPanel
            {
                Dock = DockStyle.Top,
                Height = 34,
                BackColor = Theme.BgSidebar
            };

            string[] titles =
            {
                "⚜ HIZLI KONTROL",
                "⚒ DERLEME & PACK",
                "★ SIFIRDAN KURULUM",
                "� HESAP & GM / DB",
                "⚙ AĞ, GİT & SYSERR"
            };

            int tabW = 816 / titles.Length;
            for (int i = 0; i < titles.Length; i++)
            {
                int idx = i;
                var btn = new TopTabButton(titles[i])
                {
                    Location = new Point(i * tabW, 0),
                     Width = (i == titles.Length - 1) ? (816 - i * tabW) : tabW
                };
                btn.Click += (s, e) => SelectPage(idx);
                tabButtons.Add(btn);
                strip.Controls.Add(btn);
            }

            return strip;
        }

        private Panel CreateConsoleDrawer(out RichTextBox rtb, out Label bannerLbl, out Button stopBtn)
        {
            var drawer = new BufferedPanel
            {
                Dock = DockStyle.Bottom,
                Height = 96,
                BackColor = Theme.BgConsole,
                Padding = new Padding(6, 2, 6, 4)
            };
            drawer.Paint += (s, e) =>
            {
                using (var pen = new Pen(Theme.BorderGold, 1))
                    e.Graphics.DrawLine(pen, 0, 0, drawer.Width, 0);
            };

            var header = new Panel
            {
                Dock = DockStyle.Top,
                Height = 24,
                BackColor = Color.FromArgb(22, 17, 12)
            };

            var lblConTitle = new Label
            {
                Text = "▸ CANLI KONSOL:",
                Font = Theme.FontCardTitle,
                ForeColor = Theme.GoldBright,
                AutoSize = true,
                Location = new Point(4, 4)
            };

            var localBanner = new Label
            {
                Text = "Hazır",
                Font = Theme.FontSmall,
                ForeColor = Theme.Emerald,
                AutoSize = true,
                Location = new Point(125, 5)
            };
            bannerLbl = localBanner;

            var localStop = Theme.CreateButton("■ DURDUR", ButtonStyle.Danger, 88, 22);
            localStop.Font = Theme.FontButtonSm;
            localStop.Location = new Point(540, 1);
            localStop.Enabled = false;
            localStop.Click += (s, e) => backend.StopActiveCommand();
            stopBtn = localStop;

            var btnCopy = Theme.CreateButton("KOPYALA", ButtonStyle.Secondary, 84, 22);
            btnCopy.Font = Theme.FontButtonSm;
            btnCopy.Location = new Point(632, 1);

            var btnClear = Theme.CreateButton("TEMİZLE", ButtonStyle.Secondary, 82, 22);
            btnClear.Font = Theme.FontButtonSm;
            btnClear.Location = new Point(720, 1);

            rtb = new RichTextBox
            {
                Dock = DockStyle.Fill,
                BackColor = Theme.BgConsole,
                ForeColor = Theme.TextMain,
                BorderStyle = BorderStyle.None,
                ScrollBars = RichTextBoxScrollBars.None,
                ReadOnly = true,
                Font = Theme.FontMono,
                WordWrap = false
            };

            var rtbLocal = rtb;
            btnCopy.Click += (s, e) => { if (!string.IsNullOrEmpty(rtbLocal.Text)) Clipboard.SetText(rtbLocal.Text); };
            btnClear.Click += (s, e) => rtbLocal.Clear();

            header.Controls.AddRange(new Control[] { lblConTitle, localBanner, localStop, btnCopy, btnClear });
            drawer.Controls.Add(rtb);
            Theme.AttachRichTextScrollBar(rtb, drawer);
            drawer.Controls.Add(header);
            return drawer;
        }

        private void SelectPage(int index)
        {
            if (index < 0 || index >= pages.Count) return;
            for (int i = 0; i < pages.Count; i++)
            {
                pages[i].Visible = (i == index);
                tabButtons[i].IsSelected = (i == index);
            }

            if (index == 1) pageBuild.RefreshPacks();
            else if (index == 2) pageSetup.RefreshChecklist();
            else if (index == 3) pageDbGm.RefreshTables();
            else if (index == 4) pageConfigGit.RefreshGitStatus();
        }

        private async Task RunFullE2eVerificationAndCaptureAsync(string outDir)
        {
            try
            {
                SelectPage(2);
                Refresh();
                Application.DoEvents();
                await pageSetup.ResetAndCleanInstallAsync(false);
                await PollHealthAsync();
                if (!string.IsNullOrEmpty(outDir))
                    await CaptureAllPagesAndExitAsync(outDir);
            }
            catch { Application.Exit(); }
        }

        private async Task CaptureAllPagesAndExitAsync(string outDir)
        {
            try
            {
                Directory.CreateDirectory(outDir);
                TopMost = true;
                BringToFront();
                Activate();
                await Task.Delay(700);

                for (int i = 0; i < pages.Count; i++)
                {
                    SelectPage(i);
                    Refresh();
                    Application.DoEvents();
                    await Task.Delay(550);
                    Refresh();
                    Application.DoEvents();

                    using (var bmp = new Bitmap(Width, Height))
                    {
                        bool ok = false;
                        using (var g = Graphics.FromImage(bmp))
                        {
                            IntPtr hdc = g.GetHdc();
                            try { ok = PrintWindow(Handle, hdc, 2); }
                            finally { g.ReleaseHdc(hdc); }
                        }
                        if (!ok)
                        {
                            DrawToBitmap(bmp, new Rectangle(0, 0, Width, Height));
                        }
                        bmp.Save(Path.Combine(outDir, string.Format("page_{0}.png", i)), ImageFormat.Png);
                    }
                }
            }
            catch { }
            finally { Application.Exit(); }
        }

        private void AppendConsoleLine(string text, bool isError)
        {
            if (text == null) return;
            if (!string.IsNullOrEmpty(this.captureOutputDir))
            {
                lock (logFileLock)
                {
                    try
                    {
                        Directory.CreateDirectory(this.captureOutputDir);
                        File.AppendAllText(Path.Combine(this.captureOutputDir, "live_console.log"), text + Environment.NewLine, Encoding.UTF8);
                    }
                    catch { }
                }
            }
            consoleQueue.Enqueue(Tuple.Create(text, isError));
        }

        private void FlushConsoleQueue()
        {
            if (IsDisposed || rtbConsole == null || rtbConsole.IsDisposed || consoleQueue.IsEmpty) return;
            var sb = new StringBuilder();
            bool hasError = false;
            int count = 0;
            Tuple<string, bool> item;
            while (count < 250 && consoleQueue.TryDequeue(out item))
            {
                sb.AppendLine(item.Item1);
                if (item.Item2) hasError = true;
                count++;
            }
            if (count == 0) return;
            if (rtbConsole.TextLength > 60000) rtbConsole.Clear();

            string batch = sb.ToString();
            Color lineColor = Theme.TextMain;
            if (hasError || batch.IndexOf("HATA", StringComparison.OrdinalIgnoreCase) >= 0)
                lineColor = Color.FromArgb(255, 125, 120);
            else if (batch.Contains("TAMAMLANDI") || batch.Contains("hazir"))
                lineColor = Color.FromArgb(135, 240, 170);

            rtbConsole.SelectionStart = rtbConsole.TextLength;
            rtbConsole.SelectionLength = 0;
            rtbConsole.SelectionColor = lineColor;
            rtbConsole.AppendText(batch);
            rtbConsole.ScrollToCaret();
        }

        private void UpdateTaskState(string title, bool running)
        {
            if (IsDisposed) return;
            if (InvokeRequired)
            {
                try { BeginInvoke(new Action(() => UpdateTaskState(title, running))); } catch { }
                return;
            }
            btnStopTask.Enabled = running;
            lblTaskBanner.Text = running ? ("⏳ " + title) : ("✓ " + title);
            lblTaskBanner.ForeColor = running ? Theme.GoldBright : Theme.Emerald;
            if (!running) { var _ = PollHealthAsync(); }
        }

        private async Task PollHealthAsync()
        {
            if (pollingHealth || IsDisposed) return;
            pollingHealth = true;
            try
            {
                var snap = await Task.Run(() => backend.GetHealthSnapshot());
                if (IsDisposed) return;
                pageDashboard.ApplySnapshot(snap);
                if (lblTopServerStatus != null)
                {
                    lblTopServerStatus.Text = string.Format("Oyun: {0}/7  •  Web: {1}  •  DB: {2}",
                        snap.RunningGameCoresCount,
                        snap.WebStackHealthy ? "AÇIK" : "KAPALI",
                        snap.MariaDbRunning ? "AÇIK" : "KAPALI");
                    lblTopServerStatus.ForeColor = (snap.RunningGameCoresCount == 7 && snap.WebStackHealthy)
                        ? Color.FromArgb(135, 245, 175)
                        : Theme.GoldBright;
                }
            }
            catch { }
            finally { pollingHealth = false; }
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            Theme.DrawOrnateBorder(e.Graphics, ClientRectangle, true);
        }
    }
}
