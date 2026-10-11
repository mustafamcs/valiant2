using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Windows.Forms;

namespace Valiant2Launcher
{
    internal sealed class LauncherForm : Form
    {
        private readonly string gameDirectory = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "game");
        private string BinaryDirectory { get { return Path.Combine(gameDirectory, "bin"); } }
        private readonly Label status = new Label { AutoSize = false, TextAlign = ContentAlignment.MiddleCenter, Dock = DockStyle.Top, Height = 45 };
        private readonly Button play = new Button { Text = "OYUNU BAŞLAT", Width = 240, Height = 50 };
        private readonly Button settings = new Button { Text = "AYARLAR", Width = 115, Height = 36 };
        private readonly Button folder = new Button { Text = "DOSYALAR", Width = 115, Height = 36 };

        public LauncherForm()
        {
            Text = "VALIANT2 Launcher";
            StartPosition = FormStartPosition.CenterScreen;
            FormBorderStyle = FormBorderStyle.None;
            MaximizeBox = false;
            Padding = new Padding(2);
            ClientSize = new Size(520, 330);
            BackColor = Color.FromArgb(15, 13, 12);
            ForeColor = Color.FromArgb(218, 204, 170);
            Font = new Font("Georgia", 9F);
            DoubleBuffered = true;
            Paint += PaintBackground;
            BuildInterface();
            RefreshStatus();
        }

        private void BuildInterface()
        {
            var chrome = CreateTitleBar("VALIANT2 LAUNCHER");
            var title = new Label { Text = "V A L I A N T  II", Font = new Font("Georgia", 28, FontStyle.Bold), ForeColor = Color.FromArgb(218, 174, 76), BackColor = Color.Transparent, TextAlign = ContentAlignment.BottomCenter, Dock = DockStyle.Top, Height = 92 };
            var subtitle = new Label { Text = "DOĞU'NUN SAVAŞI", Font = new Font("Georgia", 9, FontStyle.Italic), ForeColor = Color.FromArgb(151, 131, 94), BackColor = Color.Transparent, TextAlign = ContentAlignment.TopCenter, Dock = DockStyle.Top, Height = 34 };
            status.BackColor = Color.FromArgb(28, 24, 21); status.Font = new Font("Georgia", 9, FontStyle.Bold); status.Height = 40;
            var panel = new FlowLayoutPanel { Dock = DockStyle.Fill, FlowDirection = FlowDirection.TopDown, WrapContents = false, BackColor = Color.Transparent, Padding = new Padding(135, 18, 0, 0) };
            var secondary = new FlowLayoutPanel { Width = 250, Height = 48, FlowDirection = FlowDirection.LeftToRight, BackColor = Color.Transparent };
            StyleButton(play, true); StyleButton(settings, false); StyleButton(folder, false);
            play.Click += PlayClick; settings.Click += SettingsClick; folder.Click += FolderClick;
            secondary.Controls.Add(settings); secondary.Controls.Add(folder);
            panel.Controls.Add(play); panel.Controls.Add(secondary);
            Controls.Add(panel); Controls.Add(status); Controls.Add(subtitle); Controls.Add(title); Controls.Add(chrome);
        }

        private Panel CreateTitleBar(string caption)
        {
            var bar = new Panel { Dock = DockStyle.Top, Height = 36, BackColor = Color.FromArgb(24, 20, 17) };
            var text = new Label { Text = caption, Dock = DockStyle.Fill, ForeColor = Color.FromArgb(194, 151, 67), TextAlign = ContentAlignment.MiddleLeft, Padding = new Padding(12, 0, 0, 0), Font = new Font("Georgia", 9F, FontStyle.Bold) };
            var close = new Button { Text = "×", Dock = DockStyle.Right, Width = 42, FlatStyle = FlatStyle.Flat, BackColor = Color.FromArgb(87, 27, 24), ForeColor = Color.FromArgb(235, 214, 166), Font = new Font("Georgia", 14F) };
            var minimize = new Button { Text = "—", Dock = DockStyle.Right, Width = 42, FlatStyle = FlatStyle.Flat, BackColor = Color.FromArgb(38, 31, 26), ForeColor = Color.FromArgb(218, 193, 142), Font = new Font("Georgia", 10F) };
            close.FlatAppearance.BorderSize = 0; minimize.FlatAppearance.BorderSize = 0;
            close.Click += (s, e) => Close(); minimize.Click += (s, e) => WindowState = FormWindowState.Minimized;
            MouseEventHandler drag = (s, e) => { if (e.Button == MouseButtons.Left) { ReleaseCapture(); SendMessage(Handle, 0xA1, new IntPtr(2), IntPtr.Zero); } };
            bar.MouseDown += drag; text.MouseDown += drag;
            bar.Controls.Add(text); bar.Controls.Add(minimize); bar.Controls.Add(close);
            return bar;
        }

        private static void StyleButton(Button button, bool primary)
        {
            button.FlatStyle = FlatStyle.Flat;
            button.FlatAppearance.BorderSize = 1;
            button.FlatAppearance.BorderColor = Color.FromArgb(179, 137, 55);
            button.FlatAppearance.MouseOverBackColor = Color.FromArgb(105, 35, 31);
            button.FlatAppearance.MouseDownBackColor = Color.FromArgb(72, 22, 20);
            button.BackColor = primary ? Color.FromArgb(119, 36, 31) : Color.FromArgb(37, 31, 27);
            button.ForeColor = Color.FromArgb(235, 214, 166);
            button.Font = new Font("Georgia", primary ? 11F : 9F, FontStyle.Bold);
            button.Margin = new Padding(4);
        }

        private void PaintBackground(object sender, PaintEventArgs e)
        {
            using (var brush = new System.Drawing.Drawing2D.LinearGradientBrush(ClientRectangle, Color.FromArgb(37, 31, 27), Color.FromArgb(10, 9, 8), 90F)) e.Graphics.FillRectangle(brush, ClientRectangle);
            using (var pen = new Pen(Color.FromArgb(151, 111, 42), 2F)) e.Graphics.DrawRectangle(pen, 7, 7, ClientSize.Width - 15, ClientSize.Height - 15);
            using (var pen = new Pen(Color.FromArgb(72, 55, 31))) e.Graphics.DrawRectangle(pen, 12, 12, ClientSize.Width - 25, ClientSize.Height - 25);
        }

        private void RefreshStatus()
        {
            var requiredFiles = new[] { "M2Client.exe", "config.exe", "python27.dll", "granny2.dll" };
            var missing = requiredFiles.Where(x => !File.Exists(Path.Combine(BinaryDirectory, x))).Concat(new[] { "pack" }.Where(x => !Directory.Exists(Path.Combine(gameDirectory, x)))).ToArray();
            status.Text = missing.Length == 0 ? "Oyun hazır" : "Eksik dosyalar: " + string.Join(", ", missing);
            status.ForeColor = missing.Length == 0 ? Color.LightGreen : Color.OrangeRed;
            play.Enabled = missing.Length == 0;
        }

        private void PlayClick(object sender, EventArgs e)
        {
            var running = Process.GetProcessesByName("M2Client").FirstOrDefault();
            if (running != null) { if (running.MainWindowHandle != IntPtr.Zero) { ShowWindow(running.MainWindowHandle, 9); SetForegroundWindow(running.MainWindowHandle); } return; }
            Start("M2Client.exe");
            status.Text = "Oyun başlatıldı";
        }

        private void SettingsClick(object sender, EventArgs e)
        {
            Start("config.exe");
        }

        private void FolderClick(object sender, EventArgs e)
        {
            if (Directory.Exists(gameDirectory)) Process.Start("explorer.exe", gameDirectory);
        }

        private void Start(string file)
        {
            var path = Path.Combine(BinaryDirectory, file);
            if (!File.Exists(path)) { MessageBox.Show(file + " bulunamadı.", "VALIANT2", MessageBoxButtons.OK, MessageBoxIcon.Error); RefreshStatus(); return; }
            Process.Start(new ProcessStartInfo(path) { WorkingDirectory = gameDirectory, UseShellExecute = true });
        }

        [System.Runtime.InteropServices.DllImport("user32.dll")] private static extern bool ReleaseCapture();
        [System.Runtime.InteropServices.DllImport("user32.dll")] private static extern IntPtr SendMessage(IntPtr hWnd, int message, IntPtr wParam, IntPtr lParam);
        [System.Runtime.InteropServices.DllImport("user32.dll")] private static extern bool SetForegroundWindow(IntPtr hWnd);
        [System.Runtime.InteropServices.DllImport("user32.dll")] private static extern bool ShowWindow(IntPtr hWnd, int command);
    }
}
