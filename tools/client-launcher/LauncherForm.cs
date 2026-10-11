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
            FormBorderStyle = FormBorderStyle.FixedSingle;
            MaximizeBox = false;
            ClientSize = new Size(420, 245);
            BackColor = Color.FromArgb(28, 30, 36);
            ForeColor = Color.White;
            BuildInterface();
            RefreshStatus();
        }

        private void BuildInterface()
        {
            var title = new Label { Text = "VALIANT2", Font = new Font("Segoe UI", 26, FontStyle.Bold), TextAlign = ContentAlignment.MiddleCenter, Dock = DockStyle.Top, Height = 72 };
            var panel = new FlowLayoutPanel { Dock = DockStyle.Fill, FlowDirection = FlowDirection.TopDown, WrapContents = false, AutoSize = false, Padding = new Padding(85, 8, 0, 0) };
            var secondary = new FlowLayoutPanel { Width = 250, Height = 45, FlowDirection = FlowDirection.LeftToRight };
            play.BackColor = Color.FromArgb(47, 125, 225); play.ForeColor = Color.White; play.FlatStyle = FlatStyle.Flat;
            settings.FlatStyle = FlatStyle.Flat; folder.FlatStyle = FlatStyle.Flat;
            play.Click += PlayClick; settings.Click += SettingsClick; folder.Click += FolderClick;
            secondary.Controls.Add(settings); secondary.Controls.Add(folder);
            panel.Controls.Add(play); panel.Controls.Add(secondary);
            Controls.Add(panel); Controls.Add(status); Controls.Add(title);
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

        [System.Runtime.InteropServices.DllImport("user32.dll")] private static extern bool SetForegroundWindow(IntPtr hWnd);
        [System.Runtime.InteropServices.DllImport("user32.dll")] private static extern bool ShowWindow(IntPtr hWnd, int command);
    }
}
