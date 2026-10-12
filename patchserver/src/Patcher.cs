using System;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.IO.Compression;
using System.Net;
using System.Runtime.Serialization.Json;
using System.Runtime.Serialization;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

[DataContract]
public class Manifest {
    [DataMember] public int version;
    [DataMember(Name="base")] public string baseUrl;
    [DataMember] public ManifestFile[] files;
}
[DataContract]
public class ManifestFile {
    [DataMember] public string path;
    [DataMember] public long size;
    [DataMember] public string sha256;
}
[DataContract]
public class PatcherInfo {
    [DataMember] public int version;
    [DataMember] public string url;
    [DataMember] public string sha256;
}

public class PatcherForm : Form {
    const string BASE_URL = "@@BASE_URL@@";
    const string MANIFEST_URL = BASE_URL + "/update/patchlist.json";
    const string PATCHER_INFO_URL = BASE_URL + "/update/patcher.json";
    const int PATCHER_VERSION = 1;
    const string GAME_EXE = @"bin\M2Client.exe";
    const string CONFIG_EXE = @"bin\config.exe";

    static readonly Color BG      = Color.FromArgb(16, 12, 9);
    static readonly Color GOLD    = Color.FromArgb(198, 156, 78);
    static readonly Color GOLD_HI = Color.FromArgb(232, 197, 122);
    static readonly Color TXT     = Color.FromArgb(200, 186, 158);
    static readonly Color DIM     = Color.FromArgb(120, 105, 82);
    static readonly Color BAR_BG  = Color.FromArgb(42, 34, 24);
    static readonly Color BTN_BG  = Color.FromArgb(58, 44, 26);
    static readonly Color BTN_BD  = Color.FromArgb(150, 116, 56);

    Label lblStatus, lblPct, lblVer;
    Image logoImg;
    Panel pnlBarBg, pnlBar;
    Button btnStart, btnCfg;
    bool updating = false, done = false;
    int remoteVersion = 0;

    public PatcherForm() {
        FormBorderStyle = FormBorderStyle.None;
        StartPosition = FormStartPosition.CenterScreen;
        Size = new Size(760, 460);
        BackColor = BG;
        DoubleBuffered = true;
        SetStyle(ControlStyles.OptimizedDoubleBuffer | ControlStyles.AllPaintingInWmPaint | ControlStyles.UserPaint, true);
        Icon = Icon.ExtractAssociatedIcon(Application.ExecutablePath);

        var asm = System.Reflection.Assembly.GetExecutingAssembly();
        logoImg = Image.FromStream(asm.GetManifestResourceStream("logo.png"));
        var line = new Panel { Location = new Point(60, 168), Size = new Size(Width - 120, 1), BackColor = Color.FromArgb(90, 72, 40) };
        var sub = new Label { Text = "AUTO PATCHER", ForeColor = GOLD,
            Font = new Font("Georgia", 11, FontStyle.Bold), AutoSize = true, Location = new Point(38, 182) };
        var news = new Label { Text = "@@BASE_URL@@", ForeColor = DIM,
            Font = new Font("Georgia", 9, FontStyle.Underline), AutoSize = true, Location = new Point(38, 208),
            Cursor = Cursors.Hand };
        news.Click += (s, e) => { try { Process.Start("@@BASE_URL@@"); } catch { } };
        news.MouseEnter += (s, e) => news.ForeColor = GOLD_HI;
        news.MouseLeave += (s, e) => news.ForeColor = DIM;

        lblStatus = new Label { Text = "Bağlanıyor...", ForeColor = TXT,
            Font = new Font("Segoe UI", 10), AutoSize = true, Location = new Point(38, 292), MaximumSize = new Size(560, 0) };
        lblPct = new Label { Text = "", ForeColor = GOLD_HI, Font = new Font("Segoe UI", 10, FontStyle.Bold),
            AutoSize = false, Size = new Size(300, 18), Location = new Point(422, 292),
            TextAlign = ContentAlignment.MiddleRight };
        lblVer = new Label { Text = "Patcher v" + PATCHER_VERSION, ForeColor = DIM,
            Font = new Font("Segoe UI", 8), AutoSize = true, Location = new Point(38, 430) };

        pnlBarBg = new Panel { Location = new Point(38, 326), Size = new Size(684, 12), BackColor = BAR_BG };
        pnlBar = new Panel { Location = new Point(0, 0), Size = new Size(0, 12), BackColor = GOLD };
        pnlBarBg.Controls.Add(pnlBar);

        btnStart = new Button { Text = "OYNA", Location = new Point(576, 380), Size = new Size(146, 46),
            FlatStyle = FlatStyle.Flat, BackColor = BTN_BG, ForeColor = GOLD_HI,
            Font = new Font("Georgia", 13, FontStyle.Bold), Cursor = Cursors.Hand, Enabled = false };
        btnStart.FlatAppearance.BorderColor = BTN_BD;
        btnStart.FlatAppearance.BorderSize = 1;
        btnStart.FlatAppearance.MouseOverBackColor = Color.FromArgb(86, 64, 34);
        btnStart.Click += (s, e) => LaunchGame();

        btnCfg = new Button { Text = "AYARLAR", Location = new Point(416, 380), Size = new Size(146, 46),
            FlatStyle = FlatStyle.Flat, BackColor = BTN_BG, ForeColor = TXT,
            Font = new Font("Georgia", 11, FontStyle.Bold), Cursor = Cursors.Hand };
        btnCfg.FlatAppearance.BorderColor = BTN_BD;
        btnCfg.FlatAppearance.BorderSize = 1;
        btnCfg.FlatAppearance.MouseOverBackColor = Color.FromArgb(86, 64, 34);
        btnCfg.Click += (s, e) => LaunchConfig();

        var btnClose = new Button { Text = "✕", Location = new Point(716, 12), Size = new Size(30, 30),
            FlatStyle = FlatStyle.Flat, BackColor = Color.FromArgb(140, 26, 26), ForeColor = Color.FromArgb(255, 200, 180),
            Font = new Font("Segoe UI", 10, FontStyle.Bold), Cursor = Cursors.Hand };
        btnClose.FlatAppearance.BorderSize = 0;
        btnClose.FlatAppearance.MouseOverBackColor = Color.FromArgb(190, 40, 40);
        using (var gp = new GraphicsPath()) { gp.AddEllipse(0, 0, 29, 29); btnClose.Region = new Region(gp); }
        btnClose.Click += (s, e) => Application.Exit();

        var btnMin = new Button { Text = "—", Location = new Point(680, 12), Size = new Size(30, 30),
            FlatStyle = FlatStyle.Flat, BackColor = BTN_BG, ForeColor = GOLD_HI,
            Font = new Font("Segoe UI", 10, FontStyle.Bold), Cursor = Cursors.Hand };
        btnMin.FlatAppearance.BorderSize = 0;
        btnMin.FlatAppearance.MouseOverBackColor = Color.FromArgb(86, 64, 34);
        using (var gp = new GraphicsPath()) { gp.AddEllipse(0, 0, 29, 29); btnMin.Region = new Region(gp); }
        btnMin.Click += (s, e) => WindowState = FormWindowState.Minimized;

        Controls.AddRange(new Control[] { line, sub, news, lblStatus, lblPct, lblVer, pnlBarBg, btnStart, btnCfg, btnClose, btnMin });

        MouseDown += (s, e) => { if (e.Button == MouseButtons.Left) { NativeDrag(); } };

        ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12 | (SecurityProtocolType)0x3000;
        Load += async (s, e) => await Run();
    }

    [System.Runtime.InteropServices.DllImport("user32.dll")]
    static extern bool ReleaseCapture();
    [System.Runtime.InteropServices.DllImport("user32.dll")]
    static extern int SendMessage(IntPtr hWnd, int Msg, int wParam, int lParam);
    void NativeDrag() { ReleaseCapture(); SendMessage(Handle, 0xA1, 0x2, 0); }

    protected override void OnPaint(PaintEventArgs e) {
        var g = e.Graphics;
        g.InterpolationMode = InterpolationMode.HighQualityBicubic;
        g.SmoothingMode = SmoothingMode.AntiAlias;
        g.PixelOffsetMode = PixelOffsetMode.HighQuality;
        var rc = ClientRectangle;
        using (var br = new LinearGradientBrush(rc, Color.FromArgb(34, 26, 16), Color.FromArgb(9, 7, 5), LinearGradientMode.Vertical))
            g.FillRectangle(br, rc);
        if (logoImg != null) {
            int lw = 468, lh = lw * logoImg.Height / logoImg.Width;
            g.DrawImage(logoImg, (Width - lw) / 2, 26, lw, lh);
        }
        using (var pen = new Pen(Color.FromArgb(110, 88, 48)))
            g.DrawRectangle(pen, 0, 0, Width - 1, Height - 1);
        using (var pen = new Pen(Color.FromArgb(60, 48, 30)))
            g.DrawRectangle(pen, 2, 2, Width - 5, Height - 5);
        g.DrawLine(new Pen(Color.FromArgb(160, 128, 66)), 38, 258, Width - 38, 258);
        base.OnPaint(e);
    }

    void SetStatus(string t) { if (InvokeRequired) { Invoke(new Action(() => SetStatus(t))); return; } lblStatus.Text = t; }
    void SetPct(int pct, string txt) {
        if (InvokeRequired) { Invoke(new Action(() => SetPct(pct, txt))); return; }
        pnlBar.Width = (int)(pnlBarBg.Width * pct / 100.0);
        lblPct.Text = txt;
    }

    static string Sha256File(string f) {
        using (var s = File.OpenRead(f))
        using (var h = SHA256.Create())
            return BitConverter.ToString(h.ComputeHash(s)).Replace("-", "").ToLowerInvariant();
    }

    static string DownloadString(string url) {
        using (var wc = new WebClient())
            return Encoding.UTF8.GetString(wc.DownloadData(url));
    }

    static T Json<T>(string s) {
        var ser = new DataContractJsonSerializer(typeof(T));
        using (var ms = new MemoryStream(Encoding.UTF8.GetBytes(s)))
            return (T)ser.ReadObject(ms);
    }

    async Task SelfUpdate() {
        try {
            var info = Json<PatcherInfo>(DownloadString(PATCHER_INFO_URL + "?t=" + DateTime.Now.Ticks));
            if (info.version <= PATCHER_VERSION) return;
            var self = Application.ExecutablePath;
            if (!string.IsNullOrEmpty(info.sha256) && Sha256File(self) == info.sha256.ToLowerInvariant()) return;
            SetStatus("Patcher güncelleniyor...");
            var tmp = self + ".new";
            using (var wc = new WebClient()) await wc.DownloadFileTaskAsync(info.url, tmp);
            var bat = Path.Combine(Path.GetTempPath(), "patcher_swap.bat");
            File.WriteAllText(bat, "@echo off\r\ntimeout /t 1 /nobreak >nul\r\nmove /y \"" + tmp + "\" \"" + self + "\"\r\nstart \"\" \"" + self + "\"\r\ndel \"%~f0\"\r\n");
            Process.Start(new ProcessStartInfo { FileName = bat, WindowStyle = ProcessWindowStyle.Hidden, CreateNoWindow = true });
            Application.Exit();
        } catch { }
    }

    async Task Run() {
        updating = true;
        await SelfUpdate();
        if (!IsDisposed == false) return;
        try {
            SetStatus("Güncellemeler kontrol ediliyor...");
            var manifest = Json<Manifest>(DownloadString(MANIFEST_URL + "?t=" + DateTime.Now.Ticks));
            remoteVersion = manifest.version;
            var baseUrl = string.IsNullOrEmpty(manifest.baseUrl) ? BASE_URL + "/update/files/" : manifest.baseUrl;
            if (!baseUrl.EndsWith("/")) baseUrl += "/";
            var root = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "game") + "\\";

            var todo = new System.Collections.Generic.List<ManifestFile>();
            foreach (var f in manifest.files) {
                var local = Path.Combine(root, f.path.Replace('/', '\\'));
                if (!File.Exists(local) || new FileInfo(local).Length != f.size || Sha256File(local) != f.sha256.ToLowerInvariant())
                    todo.Add(f);
            }

            if (todo.Count == 0) {
                SetStatus("Client güncel. (v" + remoteVersion + ")");
                SetPct(100, "100%");
            } else {
                long totalBytes = 0, doneBytes = 0; int doneFiles = 0;
                foreach (var f in todo) totalBytes += f.size;
                var sw = System.Diagnostics.Stopwatch.StartNew();
                long lastBytes = 0; long lastTick = 0; double speed = 0;
                foreach (var f in todo) {
                    var local = Path.Combine(root, f.path.Replace('/', '\\'));
                    Directory.CreateDirectory(Path.GetDirectoryName(local));
                    SetStatus("İndiriliyor: " + f.path + "  (" + (doneFiles + 1) + "/" + todo.Count + ")");
                    using (var wc = new WebClient()) {
                        wc.DownloadProgressChanged += (s, e) => {
                            var tb = doneBytes + e.BytesReceived;
                            var tick = sw.ElapsedMilliseconds;
                            if (tick - lastTick >= 500) {
                                var inst = (tb - lastBytes) * 1000.0 / Math.Max(1, tick - lastTick);
                                speed = speed == 0 ? inst : speed * 0.6 + inst * 0.4;
                                lastBytes = tb; lastTick = tick;
                            }
                            SetPct((int)(tb * 100 / Math.Max(1, totalBytes)),
                                (tb / 1048576) + " MB / " + (totalBytes / 1048576) + " MB  ·  " +
                                (speed / 1048576).ToString("0.0") + " MB/s");
                        };
                        await wc.DownloadFileTaskAsync(baseUrl + f.path.Replace(" ", "%20"), local);
                    }
                    if (Sha256File(local) != f.sha256.ToLowerInvariant()) {
                        SetStatus("Doğrulama hatası: " + f.path);
                        btnStart.Enabled = false; return;
                    }
                    doneBytes += f.size; doneFiles++;
                    SetPct((int)(doneBytes * 100 / Math.Max(1, totalBytes)), doneFiles + "/" + todo.Count);
                }
                SetStatus("Güncelleme tamamlandı. (v" + remoteVersion + ")");
            }
            btnStart.Enabled = true;
            done = true;
        } catch (Exception ex) {
            SetStatus("Sunucuya bağlanılamadı: " + ex.Message);
            btnStart.Text = "TEKRAR DENE";
            btnStart.Enabled = true;
            btnStart.Click -= RetryLaunch;
            btnStart.Click += RetryLaunch;
        } finally { updating = false; }
    }

    void RetryLaunch(object s, EventArgs e) {
        btnStart.Click -= RetryLaunch;
        btnStart.Text = "OYNA"; btnStart.Enabled = false;
        Task.Run(async () => await Run());
    }

    void EnsureDefaultCfg() {
        var dir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "game");
        var cfg = Path.Combine(dir, "metin2.cfg");
        var def =
            "WIDTH\t1280\r\nHEIGHT\t1024\r\nBPP\t32\r\nFREQUENCY\t120\r\n" +
            "SOFTWARE_CURSOR\t0\r\nOBJECT_CULLING\t1\r\nVISIBILITY\t3\r\n" +
            "MUSIC_VOLUME\t1.000\r\nVOICE_VOLUME\t3\r\nGAMMA\t1\r\n" +
            "IS_SAVE_ID\t0\r\nSAVE_ID\t0\r\nDECOMPRESSED_TEXTURE\t0\r\n" +
            "WINDOWED\t1\r\nUSE_DEFAULT_IME\t0\r\nSOFTWARE_TILING\t0\r\n" +
            "SHADOW_LEVEL\t3\r\nTEXT_OUTLINE\t1\r\nAFFECT_ICONS\t1\r\n" +
            "FIELD_OF_VIEW_RATE\t0.87\r\nHIGHLIGHT_ANIMATION\t1\r\n" +
            "HIDE_PETS\t0\r\nHIDE_MOUNTS\t0\r\nHIDE_SHOPS\t0\r\nHIDE_NPC\t0\r\n" +
            "ANIMATION_TYPE\t0\r\nFONT_TYPE\t0\r\nHIDE_EFFECTS\t0\r\nHIDE_TOOLTIP_EMOJIS\t1\r\n" +
            "METINSTONE_SCALE_RATE\t0.0\r\nDAMAGE_TEXTURE_SCALE_RATE\t0.1\r\n" +
            "SELECTED_SKYBOX_TYPE\t1\r\nENTITY_SHOW_DISTANCE\t6500\r\n" +
            "DAMAGE_TYPE\t2\r\nDAMAGE_TYPE_RENEWED\t0\r\n" +
            "HIDE_EVENT_IMAGE\t1\r\nANIMATED_LOADING\t1\r\n";
        Directory.CreateDirectory(dir);
        if (!File.Exists(cfg)) File.WriteAllText(cfg, def);
    }

    void LaunchGame() {
        if (!done) { Task.Run(async () => await Run()); return; }
        EnsureDefaultCfg();
        var dir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "game");
        var exe = Path.Combine(dir, GAME_EXE);
        if (File.Exists(exe)) {
            Process.Start(new ProcessStartInfo { FileName = exe, WorkingDirectory = dir });
            Application.Exit();
        } else SetStatus("Oyun dosyası bulunamadı: " + GAME_EXE);
    }

    void LaunchConfig() {
        EnsureDefaultCfg();
        var dir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "game");
        var exe = Path.Combine(dir, CONFIG_EXE);
        if (File.Exists(exe)) Process.Start(new ProcessStartInfo { FileName = exe, WorkingDirectory = dir });
        else SetStatus("Ayarlar dosyası bulunamadı: " + CONFIG_EXE);
    }
}

static class Program {
    [STAThread]
    static void Main() {
        Application.EnableVisualStyles();
        Application.Run(new PatcherForm());
    }
}
