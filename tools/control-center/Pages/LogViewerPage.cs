using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace Valiant2ControlCenter.Pages
{
    internal sealed class LogViewerPage : BufferedPanel
    {
        private readonly BackendService backend;
        private readonly ListBox lstLogFiles;
        private readonly RichTextBox rtbLogContent;
        private readonly TextBox txtFilter;
        private readonly CheckBox chkOnlyNonEmpty;
        private readonly Label lblSelectedFile;
        private readonly List<string> logFilePaths = new List<string>();

        public LogViewerPage(BackendService backend)
        {
            this.backend = backend;
            Dock = DockStyle.Fill;
            BackColor = Theme.BgMain;
            Padding = new Padding(16);

            var topBar = new BufferedPanel
            {
                Dock = DockStyle.Top,
                Height = 52,
                BackColor = Theme.BgCard,
                DrawCardBorder = true,
                Padding = new Padding(12, 8, 12, 8)
            };

            var lblTitle = new Label
            {
                Text = "SYSERR / SYSLOG HATA İZLEYİCİ",
                Font = Theme.FontCardTitle,
                ForeColor = Theme.GoldBright,
                AutoSize = true,
                Location = new Point(12, 15),
                UseMnemonic = false
            };

            chkOnlyNonEmpty = new CheckBox
            {
                Text = "Sadece Dolu Dosyalar",
                ForeColor = Theme.Gold,
                Font = Theme.FontSmall,
                Checked = false,
                AutoSize = true,
                Location = new Point(290, 16),
                UseMnemonic = false
            };
            chkOnlyNonEmpty.CheckedChanged += (s, e) => RefreshLogList();

            var lblSearch = new Label
            {
                Text = "Filtre:",
                Font = Theme.FontSmall,
                ForeColor = Theme.TextMuted,
                AutoSize = true,
                Location = new Point(455, 17),
                UseMnemonic = false
            };

            txtFilter = Theme.CreateTextBox("");
            txtFilter.Location = new Point(498, 14);
            txtFilter.Size = new Size(175, 22);
            txtFilter.TextChanged += (s, e) => ReloadSelectedLog();

            var btnScanSyserr = Theme.CreateButton("🔍 TÜM SYSERR TARA", ButtonStyle.PrimaryGold, 175, 30);
            btnScanSyserr.Location = new Point(686, 10);
            btnScanSyserr.Font = new Font("Georgia", 8.0F, FontStyle.Bold);
            btnScanSyserr.Click += (s, e) => ScanAllSyserrs();

            var btnRefresh = Theme.CreateButton("↻ YENİLE", ButtonStyle.Secondary, 100, 30);
            btnRefresh.Location = new Point(868, 10);
            btnRefresh.Font = new Font("Georgia", 8.0F, FontStyle.Bold);
            btnRefresh.Click += (s, e) => { RefreshLogList(); ReloadSelectedLog(); };

            topBar.Controls.AddRange(new Control[] { lblTitle, chkOnlyNonEmpty, lblSearch, txtFilter, btnScanSyserr, btnRefresh });

            var split = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 2,
                RowCount = 1,
                BackColor = Color.Transparent,
                Padding = new Padding(0, 10, 0, 0)
            };
            split.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 290F));
            split.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));

            var leftCard = new BufferedPanel
            {
                Dock = DockStyle.Fill,
                BackColor = Theme.BgCard,
                DrawCardBorder = true,
                Margin = new Padding(0, 0, 6, 0),
                Padding = new Padding(10)
            };

            var lblFilesHeader = new Label
            {
                Text = "LOG & SYSERR DOSYALARI",
                Dock = DockStyle.Top,
                Height = 24,
                Font = Theme.FontCardTitle,
                ForeColor = Theme.GoldBright
            };

            lstLogFiles = new ListBox
            {
                Dock = DockStyle.Fill,
                BackColor = Theme.BgInput,
                ForeColor = Theme.TextMain,
                BorderStyle = BorderStyle.None,
                Font = Theme.FontBody,
                IntegralHeight = false
            };
            lstLogFiles.SelectedIndexChanged += (s, e) => ReloadSelectedLog();

            var btnClearSelected = Theme.CreateButton("SEÇİLİ LOGU SIFIRLA", ButtonStyle.Danger, 260, 30);
            btnClearSelected.Dock = DockStyle.Bottom;
            btnClearSelected.Font = new Font("Georgia", 8.25F, FontStyle.Bold);
            btnClearSelected.Click += (s, e) => ClearSelectedLogFile();

            leftCard.Controls.Add(lstLogFiles);
            leftCard.Controls.Add(lblFilesHeader);
            leftCard.Controls.Add(btnClearSelected);

            var rightCard = new BufferedPanel
            {
                Dock = DockStyle.Fill,
                BackColor = Theme.BgCard,
                DrawCardBorder = true,
                Margin = new Padding(6, 0, 0, 0),
                Padding = new Padding(10)
            };

            lblSelectedFile = new Label
            {
                Text = "Bir log dosyası seçin veya 'Tüm SYSERR Taraması' butonuna tıklayın.",
                Dock = DockStyle.Top,
                Height = 24,
                Font = Theme.FontBodyBold,
                ForeColor = Theme.Gold
            };

            rtbLogContent = new RichTextBox
            {
                Dock = DockStyle.Fill,
                BackColor = Theme.BgConsole,
                ForeColor = Theme.TextMain,
                BorderStyle = BorderStyle.None,
                ReadOnly = true,
                Font = Theme.FontMono,
                WordWrap = false
            };

            rightCard.Controls.Add(rtbLogContent);
            rightCard.Controls.Add(lblSelectedFile);

            split.Controls.Add(leftCard, 0, 0);
            split.Controls.Add(rightCard, 1, 0);

            Controls.Add(split);
            Controls.Add(topBar);

            RefreshLogList();
        }

        public void RefreshLogList()
        {
            int prevIdx = lstLogFiles.SelectedIndex;
            lstLogFiles.Items.Clear();
            logFilePaths.Clear();

            var candidates = new List<Tuple<string, string>>();
            candidates.Add(Tuple.Create("Client • syserr.txt", Path.Combine(backend.ProjectRoot, @"runtime\client\game\syserr.txt")));

            string srvRoot = Path.Combine(backend.ProjectRoot, @"runtime\server\main\srv1");
            string[] cores =
            {
                @"db", @"auth",
                @"chan\ch1\core1", @"chan\ch1\core2", @"chan\ch1\core3", @"chan\ch1\core4",
                @"chan\ch99\core99"
            };
            foreach (var c in cores)
            {
                string labelPrefix = c.Replace(@"chan\", "").Replace('\\', '/');
                string dir = Path.Combine(srvRoot, c);
                string syserrFile = File.Exists(Path.Combine(dir, "syserr.txt")) ? Path.Combine(dir, "syserr.txt") : Path.Combine(dir, "syserr");
                string syslogFile = File.Exists(Path.Combine(dir, "syslog.txt")) ? Path.Combine(dir, "syslog.txt") : Path.Combine(dir, "syslog");
                string ptsFile    = File.Exists(Path.Combine(dir, "PTS.txt"))    ? Path.Combine(dir, "PTS.txt")    : Path.Combine(dir, "PTS");
                candidates.Add(Tuple.Create(labelPrefix + " • syserr.txt", syserrFile));
                candidates.Add(Tuple.Create(labelPrefix + " • syslog.txt", syslogFile));
                candidates.Add(Tuple.Create(labelPrefix + " • PTS.txt", ptsFile));
            }

            string nginxErr = Path.Combine(backend.ProjectRoot, @"runtime\dependencies\nginx\logs\error.log");
            candidates.Add(Tuple.Create("nginx • error.log", nginxErr));

            foreach (var item in candidates)
            {
                var fi = new FileInfo(item.Item2);
                long len = fi.Exists ? fi.Length : 0;
                if (chkOnlyNonEmpty.Checked && len == 0) continue;

                string badge = !fi.Exists ? " (Yok)" : (len == 0 ? " (Temiz - 0 B)" : string.Format(" ({0:0.0} KB)", len / 1024.0));
                lstLogFiles.Items.Add(item.Item1 + badge);
                logFilePaths.Add(item.Item2);
            }

            if (lstLogFiles.Items.Count > 0)
            {
                lstLogFiles.SelectedIndex = Math.Max(0, Math.Min(prevIdx, lstLogFiles.Items.Count - 1));
            }
        }

        private void ReloadSelectedLog()
        {
            int idx = lstLogFiles.SelectedIndex;
            if (idx < 0 || idx >= logFilePaths.Count) return;
            string path = logFilePaths[idx];
            lblSelectedFile.Text = path;

            if (!File.Exists(path))
            {
                rtbLogContent.Text = "(Dosya henüz oluşmamış - Hata yok)";
                return;
            }

            try
            {
                string content;
                using (var fs = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                {
                    if (fs.Length > 256 * 1024)
                        fs.Seek(-256 * 1024, SeekOrigin.End);
                    using (var sr = new StreamReader(fs, Encoding.UTF8))
                        content = sr.ReadToEnd();
                }

                string filter = txtFilter.Text.Trim();
                if (!string.IsNullOrEmpty(filter))
                {
                    var lines = content.Split(new[] { "\r\n", "\n" }, StringSplitOptions.None)
                        .Where(l => l.IndexOf(filter, StringComparison.OrdinalIgnoreCase) >= 0);
                    content = string.Join(Environment.NewLine, lines);
                }

                rtbLogContent.Text = string.IsNullOrWhiteSpace(content) ? "(Dosya boş — Temiz)" : content;
                rtbLogContent.SelectionStart = rtbLogContent.TextLength;
                rtbLogContent.ScrollToCaret();
            }
            catch (Exception ex)
            {
                rtbLogContent.Text = "Dosya okunamadı: " + ex.Message;
            }
        }

        private void ScanAllSyserrs()
        {
            var sb = new StringBuilder();
            sb.AppendLine("=== TÜM SYSERR DOSYALARI ÖZET TARAMASI ===");
            sb.AppendLine("Tarih: " + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
            sb.AppendLine();

            int nonEmpty = 0;
            for (int i = 0; i < logFilePaths.Count; i++)
            {
                string p = logFilePaths[i];
                if (!p.EndsWith("syserr", StringComparison.OrdinalIgnoreCase) &&
                    !p.EndsWith("syserr.txt", StringComparison.OrdinalIgnoreCase))
                    continue;

                if (File.Exists(p))
                {
                    var fi = new FileInfo(p);
                    if (fi.Length > 0)
                    {
                        nonEmpty++;
                        sb.AppendLine("------------------------------------------------------------------");
                        sb.AppendLine("[!] " + p + " (" + fi.Length + " bayt)");
                        sb.AppendLine("------------------------------------------------------------------");
                        try
                        {
                            using (var fs = new FileStream(p, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                            using (var sr = new StreamReader(fs, Encoding.UTF8))
                                sb.AppendLine(sr.ReadToEnd().Trim());
                        }
                        catch (Exception ex) { sb.AppendLine("Okuma hatası: " + ex.Message); }
                        sb.AppendLine();
                    }
                }
            }

            if (nonEmpty == 0)
                sb.AppendLine("✓ Harika! Hiçbir sunucu core'unda veya istemcide syserr kaydı bulunmuyor (Tamamı 0 bayt / temiz).");

            lblSelectedFile.Text = "Tüm SYSERR Taraması Sonucu (" + nonEmpty + " dosyada kayıt var)";
            rtbLogContent.Text = sb.ToString();
        }

        private void ClearSelectedLogFile()
        {
            int idx = lstLogFiles.SelectedIndex;
            if (idx < 0 || idx >= logFilePaths.Count) return;
            string path = logFilePaths[idx];
            if (!File.Exists(path)) return;

            try
            {
                using (var fs = new FileStream(path, FileMode.Truncate, FileAccess.Write, FileShare.ReadWrite)) { }
                RefreshLogList();
                ReloadSelectedLog();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Log dosyası sıfırlanamadı (süreç tarafından kilitli olabilir): " + ex.Message, "Bilgi", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }
    }
}
