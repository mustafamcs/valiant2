using System;
using System.Collections.Generic;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Windows.Forms;

namespace Valiant2Config
{
    internal sealed class SettingSpec
    {
        public string Key, Label, Category, Default;
        public decimal Minimum, Maximum, Increment;
        public int Decimals;
        public bool Text;

        public SettingSpec(string key, string label, string category, string value, decimal min, decimal max, decimal increment = 1, int decimals = 0)
        {
            Key = key; Label = label; Category = category; Default = value; Minimum = min; Maximum = max; Increment = increment; Decimals = decimals;
        }

        public SettingSpec(string key, string label, string category, string value)
        {
            Key = key; Label = label; Category = category; Default = value; Text = true;
        }
    }

    internal sealed class ClientConfig
    {
        public static readonly SettingSpec[] Specs = {
            new SettingSpec("WIDTH", "Genişlik", "Ekran", "1280", 800, 16384),
            new SettingSpec("HEIGHT", "Yükseklik", "Ekran", "720", 600, 16384),
            new SettingSpec("BPP", "Renk derinliği", "Ekran", "32", 16, 32, 16),
            new SettingSpec("FREQUENCY", "Yenileme hızı / FPS", "Ekran", "60", 30, 1000),
            new SettingSpec("WINDOWED", "Pencere modu", "Ekran", "0", 0, 1),
            new SettingSpec("GAMMA", "Gamma", "Ekran", "5", 1, 5),
            new SettingSpec("FIELD_OF_VIEW_RATE", "Görüş alanı oranı", "Ekran", "0.00", -1, 1, 0.05m, 2),
            new SettingSpec("MUSIC_VOLUME", "Müzik sesi", "Ses", "1.000", 0, 1, 0.05m, 3),
            new SettingSpec("VOICE_VOLUME", "Efekt sesi", "Ses", "5", 0, 5),
            new SettingSpec("SOFTWARE_CURSOR", "Yazılımsal imleç", "Temel", "0", 0, 1),
            new SettingSpec("OBJECT_CULLING", "Nesne ayıklama", "Temel", "1", 0, 1),
            new SettingSpec("VISIBILITY", "Görüş mesafesi seviyesi", "Temel", "3", 0, 5),
            new SettingSpec("USE_DEFAULT_IME", "Sistem IME", "Temel", "0", 0, 1),
            new SettingSpec("SOFTWARE_TILING", "Yazılımsal döşeme", "Temel", "0", 0, 2),
            new SettingSpec("DECOMPRESSED_TEXTURE", "Açılmış dokular", "Temel", "0", 0, 1),
            new SettingSpec("IS_SAVE_ID", "Kullanıcı adını kaydet", "Temel", "0", 0, 1),
            new SettingSpec("SAVE_ID", "Kayıtlı kullanıcı adı", "Temel", "0"),
            new SettingSpec("SHADOW_LEVEL", "Gölge seviyesi", "Grafik", "5", 0, 5),
            new SettingSpec("TEXT_OUTLINE", "İsim kenarlığı", "Grafik", "1", 0, 1),
            new SettingSpec("AFFECT_ICONS", "Etki simgeleri", "Grafik", "1", 0, 1),
            new SettingSpec("HIGHLIGHT_ANIMATION", "Vurgu animasyonu", "Grafik", "1", 0, 1),
            new SettingSpec("HIDE_EFFECTS", "Efektleri gizle", "Grafik", "0", 0, 1),
            new SettingSpec("HIDE_TOOLTIP_EMOJIS", "Emoji ipuçlarını gizle", "Grafik", "1", 0, 1),
            new SettingSpec("METINSTONE_SCALE_RATE", "Metin taşı ölçeği", "Grafik", "0.0", 0, 1, 0.1m, 1),
            new SettingSpec("DAMAGE_TEXTURE_SCALE_RATE", "Hasar yazısı ölçeği", "Grafik", "0.0", 0, 1, 0.1m, 1),
            new SettingSpec("SELECTED_SKYBOX_TYPE", "Gökyüzü tipi", "Grafik", "0", 0, 20),
            new SettingSpec("ANIMATION_TYPE", "Animasyon tipi", "Grafik", "5", 0, 20),
            new SettingSpec("FONT_TYPE", "Yazı tipi", "Grafik", "0", 0, 20),
            new SettingSpec("ENTITY_SHOW_DISTANCE", "Varlık mesafesi", "Optimizasyon", "6500", 2500, 6500, 2000),
            new SettingSpec("MAP_LOADING_DISTANCE", "Harita yükleme mesafesi", "Optimizasyon", "0.0", 0, 10000, 100, 1),
            new SettingSpec("HIDE_PETS", "Petleri gizle", "Gizleme", "0", 0, 1),
            new SettingSpec("HIDE_MOUNTS", "Binekleri gizle", "Gizleme", "0", 0, 1),
            new SettingSpec("HIDE_SHOPS", "Pazarları gizle", "Gizleme", "0", 0, 1),
            new SettingSpec("HIDE_NPC", "NPC'leri gizle", "Gizleme", "0", 0, 1),
            new SettingSpec("VIEW_CHAT", "Sohbeti göster", "Arayüz", "1", 0, 1),
            new SettingSpec("ALWAYS_VIEW_NAME", "İsimleri göster", "Arayüz", "1", 0, 1),
            new SettingSpec("SHOW_DAMAGE", "Hasarı göster", "Arayüz", "1", 0, 1),
            new SettingSpec("SHOW_SALESTEXT", "Pazar yazılarını göster", "Arayüz", "1", 0, 1),
            new SettingSpec("SHOW_MOBAIFLAG", "Canavar tipini göster", "Arayüz", "1", 0, 1),
            new SettingSpec("SHOW_MOBLEVEL", "Canavar seviyesini göster", "Arayüz", "1", 0, 1),
            new SettingSpec("DAMAGE_TYPE", "Hasar tipi", "Arayüz", "0", 0, 20),
            new SettingSpec("DAMAGE_TYPE_RENEWED", "Yeni hasar görünümü", "Arayüz", "0", 0, 1),
            new SettingSpec("HIDE_EVENT_IMAGE", "Etkinlik görselini gizle", "Arayüz", "1", 0, 1),
            new SettingSpec("ANIMATED_LOADING", "Animasyonlu yükleme", "Arayüz", "1", 0, 1)
        };

        public readonly Dictionary<string, string> Values = Specs.ToDictionary(x => x.Key, x => x.Default, StringComparer.OrdinalIgnoreCase);
        private readonly Dictionary<string, string> unknown = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);

        public static ClientConfig Load(string path)
        {
            var config = new ClientConfig();
            if (!File.Exists(path)) return config;
            foreach (var raw in File.ReadAllLines(path))
            {
                var parts = raw.Trim().Split((char[])null, 2, StringSplitOptions.RemoveEmptyEntries);
                if (parts.Length != 2) continue;
                if (config.Values.ContainsKey(parts[0])) config.Values[parts[0]] = parts[1].Trim();
                else config.unknown[parts[0]] = parts[1].Trim();
            }
            return config;
        }

        public bool Validate()
        {
            foreach (var spec in Specs)
            {
                var value = Values[spec.Key];
                if (spec.Text)
                {
                    if (value.Length > 19 || value.Any(char.IsWhiteSpace)) return false;
                    continue;
                }
                decimal number;
                if (!decimal.TryParse(value, NumberStyles.Float, CultureInfo.InvariantCulture, out number) || number < spec.Minimum || number > spec.Maximum) return false;
            }
            return true;
        }

        public void Save(string path)
        {
            if (!Validate()) throw new InvalidDataException("Bir veya daha fazla ayar geçersiz.");
            var lines = Specs.Select(spec => spec.Key + "\t\t" + Values[spec.Key]).ToList();
            lines.AddRange(unknown.Where(x => !Values.ContainsKey(x.Key)).Select(x => x.Key + "\t\t" + x.Value));
            File.WriteAllLines(path, lines);
        }
    }

    internal sealed class DisplayMode
    {
        public int Width, Height, Bpp, Frequency;
        public override string ToString() { return Width + " x " + Height + "  " + Bpp + " bit  " + Frequency + " Hz"; }
    }

    internal sealed class ChoicePopup : Form
    {
        private const int PageSize = 12;
        private readonly IList<object> items;
        private readonly FlowLayoutPanel list;
        private readonly Label pageLabel;
        private int page;
        public int SelectedIndex = -1;

        public ChoicePopup(IList<object> items, int selectedIndex, Point location, int itemWidth)
        {
            this.items = items; SelectedIndex = selectedIndex; page = selectedIndex < 0 ? 0 : selectedIndex / PageSize;
            FormBorderStyle = FormBorderStyle.None; StartPosition = FormStartPosition.Manual; ShowInTaskbar = false; TopMost = true;
            BackColor = Color.FromArgb(20, 17, 15);
            var rows = Math.Min(PageSize, Math.Max(1, items.Count));
            ClientSize = new Size(Math.Max(itemWidth, 220) + 4, rows * 29 + (items.Count > PageSize ? 34 : 4));
            var area = Screen.FromPoint(location).WorkingArea;
            Location = new Point(Math.Max(area.Left, Math.Min(location.X, area.Right - Width)), location.Y + Height <= area.Bottom ? location.Y : Math.Max(area.Top, location.Y - Height - 28));
            list = new FlowLayoutPanel { Dock = DockStyle.Fill, FlowDirection = FlowDirection.TopDown, WrapContents = false, Padding = new Padding(2), BackColor = BackColor };
            if (items.Count > PageSize)
            {
                var footer = new Panel { Dock = DockStyle.Bottom, Height = 32, BackColor = Color.FromArgb(29, 24, 20) };
                var previous = PageButton("‹", DockStyle.Left); var next = PageButton("›", DockStyle.Right);
                pageLabel = new Label { Dock = DockStyle.Fill, TextAlign = ContentAlignment.MiddleCenter, ForeColor = Color.FromArgb(218, 174, 76), Font = new Font("Georgia", 9F, FontStyle.Bold) };
                previous.Click += (s, e) => ChangePage(-1); next.Click += (s, e) => ChangePage(1);
                footer.Controls.Add(pageLabel); footer.Controls.Add(previous); footer.Controls.Add(next); Controls.Add(footer);
            }
            Controls.Add(list); BuildPage();
            MouseWheel += (s, e) => ChangePage(e.Delta > 0 ? -1 : 1);
            Deactivate += (s, e) => { if (DialogResult == DialogResult.None) { DialogResult = DialogResult.Cancel; Close(); } };
        }

        private Button PageButton(string text, DockStyle dock)
        {
            var button = new Button { Text = text, Dock = dock, Width = 48, FlatStyle = FlatStyle.Flat, BackColor = Color.FromArgb(54, 42, 31), ForeColor = Color.FromArgb(218, 174, 76), Font = new Font("Georgia", 13F, FontStyle.Bold) };
            button.FlatAppearance.BorderColor = Color.FromArgb(116, 88, 43); return button;
        }

        private void ChangePage(int delta)
        {
            var count = Math.Max(1, (int)Math.Ceiling(items.Count / (double)PageSize)); page = (page + delta + count) % count; BuildPage();
        }

        private void BuildPage()
        {
            list.Controls.Clear(); var start = page * PageSize; var end = Math.Min(items.Count, start + PageSize);
            for (var i = start; i < end; i++)
            {
                var index = i;
                var button = new Button { Text = items[i].ToString(), Width = ClientSize.Width - 6, Height = 27, Margin = new Padding(0), FlatStyle = FlatStyle.Flat, BackColor = i == SelectedIndex ? Color.FromArgb(105, 35, 31) : Color.FromArgb(39, 33, 28), ForeColor = Color.FromArgb(232, 216, 180), TextAlign = ContentAlignment.MiddleLeft, Font = new Font("Georgia", 9F) };
                button.FlatAppearance.BorderColor = Color.FromArgb(116, 88, 43); button.FlatAppearance.MouseOverBackColor = Color.FromArgb(105, 35, 31);
                button.Click += (s, e) => { SelectedIndex = index; DialogResult = DialogResult.OK; Close(); }; list.Controls.Add(button);
            }
            if (pageLabel != null) pageLabel.Text = (page + 1) + " / " + Math.Max(1, (int)Math.Ceiling(items.Count / (double)PageSize));
        }
    }

    internal sealed class DarkChoice : Control
    {
        public readonly List<object> Items = new List<object>();
        private int selectedIndex = -1;
        public event EventHandler SelectedIndexChanged;
        public int SelectedIndex { get { return selectedIndex; } set { var next = Items.Count == 0 ? -1 : Math.Max(0, Math.Min(value, Items.Count - 1)); if (selectedIndex == next) return; selectedIndex = next; Invalidate(); if (SelectedIndexChanged != null) SelectedIndexChanged(this, EventArgs.Empty); } }
        public object SelectedItem { get { return selectedIndex >= 0 && selectedIndex < Items.Count ? Items[selectedIndex] : null; } }

        public DarkChoice()
        {
            Height = 28; DoubleBuffered = true; Cursor = Cursors.Hand; TabStop = true;
            BackColor = Color.FromArgb(39, 33, 28); ForeColor = Color.FromArgb(232, 216, 180);
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            using (var border = new Pen(Focused ? Color.FromArgb(211, 162, 62) : Color.FromArgb(116, 88, 43))) e.Graphics.DrawRectangle(border, 0, 0, Width - 1, Height - 1);
            var arrowWidth = 34;
            using (var arrowBackground = new SolidBrush(Color.FromArgb(54, 42, 31))) e.Graphics.FillRectangle(arrowBackground, Width - arrowWidth, 1, arrowWidth - 1, Height - 2);
            using (var separator = new Pen(Color.FromArgb(116, 88, 43))) e.Graphics.DrawLine(separator, Width - arrowWidth, 1, Width - arrowWidth, Height - 2);
            TextRenderer.DrawText(e.Graphics, SelectedItem == null ? "" : SelectedItem.ToString(), Font, new Rectangle(10, 0, Width - arrowWidth - 12, Height), ForeColor, TextFormatFlags.Left | TextFormatFlags.VerticalCenter | TextFormatFlags.EndEllipsis);
            TextRenderer.DrawText(e.Graphics, "▼", new Font("Segoe UI Symbol", 8, FontStyle.Bold), new Rectangle(Width - arrowWidth, 0, arrowWidth, Height), Color.FromArgb(218, 174, 76), TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter);
        }

        protected override void OnMouseDown(MouseEventArgs e)
        {
            base.OnMouseDown(e); Focus();
            if (Items.Count == 0 || e.Button != MouseButtons.Left) return;
            ShowDropDown();
        }

        private void ShowDropDown()
        {
            using (var popup = new ChoicePopup(Items, selectedIndex, PointToScreen(new Point(0, Height)), Width))
            {
                if (popup.ShowDialog(FindForm()) == DialogResult.OK) SelectedIndex = popup.SelectedIndex;
            }
            Focus();
        }

        protected override void OnMouseWheel(MouseEventArgs e)
        {
            if (Items.Count == 0) return;
            SelectedIndex = e.Delta > 0 ? (selectedIndex <= 0 ? Items.Count - 1 : selectedIndex - 1) : (selectedIndex + 1) % Items.Count;
        }

        protected override bool IsInputKey(Keys keyData) { return keyData == Keys.Up || keyData == Keys.Down || keyData == Keys.Enter || keyData == Keys.Space || base.IsInputKey(keyData); }
        protected override void OnKeyDown(KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Up) OnMouseWheel(new MouseEventArgs(MouseButtons.None, 0, 0, 0, 120));
            else if (e.KeyCode == Keys.Down) OnMouseWheel(new MouseEventArgs(MouseButtons.None, 0, 0, 0, -120));
            else if (e.KeyCode == Keys.Enter || e.KeyCode == Keys.Space) ShowDropDown();
            else base.OnKeyDown(e);
        }
    }

    internal sealed class BufferedPanel : Panel
    {
        public BufferedPanel()
        {
            SetStyle(ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw, true);
            UpdateStyles();
        }
    }

    internal sealed class BufferedTable : TableLayoutPanel
    {
        public BufferedTable()
        {
            SetStyle(ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw, true);
            UpdateStyles();
        }
    }

    internal sealed class ConfigForm : Form
    {
        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
        private struct DevMode
        {
            [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)] public string DeviceName;
            public short SpecVersion, DriverVersion, Size, DriverExtra;
            public int Fields, PositionX, PositionY, DisplayOrientation, DisplayFixedOutput;
            public short Color, Duplex, YResolution, TTOption, Collate;
            [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)] public string FormName;
            public short LogPixels;
            public int BitsPerPel, PelsWidth, PelsHeight, DisplayFlags, DisplayFrequency, ICMMethod, ICMIntent, MediaType, DitherType, Reserved1, Reserved2, PanningWidth, PanningHeight;
        }

        [DllImport("user32.dll", CharSet = CharSet.Ansi)]
        private static extern bool EnumDisplaySettings(string deviceName, int modeNum, ref DevMode devMode);
        [DllImport("user32.dll")] private static extern bool ReleaseCapture();
        [DllImport("user32.dll")] private static extern IntPtr SendMessage(IntPtr hWnd, int message, IntPtr wParam, IntPtr lParam);

        private static readonly HashSet<string> ExternalKeys = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
        {
            "WINDOWED", "GAMMA", "MUSIC_VOLUME", "VOICE_VOLUME", "SOFTWARE_CURSOR", "OBJECT_CULLING", "VISIBILITY", "USE_DEFAULT_IME", "SOFTWARE_TILING", "DECOMPRESSED_TEXTURE"
        };
        private readonly string path;
        private readonly ClientConfig config;
        private readonly Dictionary<string, Control> editors = new Dictionary<string, Control>(StringComparer.OrdinalIgnoreCase);
        private readonly List<DisplayMode> displayModes = new List<DisplayMode>();
        private readonly DarkChoice screenSize = new DarkChoice { Dock = DockStyle.Fill };
        private readonly DarkChoice colorDepth = new DarkChoice { Dock = DockStyle.Fill };
        private readonly DarkChoice refreshRate = new DarkChoice { Dock = DockStyle.Fill };
        private bool updatingDisplayModes;

        public ConfigForm(string path)
        {
            this.path = path;
            config = ClientConfig.Load(path);
            Text = "VALIANT2 Ayarları";
            StartPosition = FormStartPosition.CenterScreen;
            FormBorderStyle = FormBorderStyle.None;
            Padding = new Padding(2);
            MinimumSize = new Size(680, 700);
            Size = new Size(720, 760);
            BackColor = Color.FromArgb(18, 16, 14);
            ForeColor = Color.FromArgb(218, 204, 170);
            Font = new Font("Georgia", 9F);
            DoubleBuffered = true;
            SetStyle(ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw, true);
            BuildInterface();
        }

        private void BuildInterface()
        {
            var panel = new BufferedPanel { Dock = DockStyle.Fill, AutoScroll = false, BackColor = Color.FromArgb(18, 16, 14) };
            var table = new BufferedTable { AutoSize = true, AutoSizeMode = AutoSizeMode.GrowAndShrink, ColumnCount = 2, Dock = DockStyle.Top, Padding = new Padding(22), BackColor = Color.FromArgb(18, 16, 14), ForeColor = Color.FromArgb(218, 204, 170) };
            table.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 58));
            table.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 42));
            AddHeading(table, "Ekran");
            StyleEditor(screenSize); StyleEditor(colorDepth); StyleEditor(refreshRate);
            AddRow(table, "Ekran boyutu", screenSize);
            AddRow(table, "Renk derinliği", colorDepth);
            AddRow(table, "Yenileme hızı", refreshRate);
            LoadDisplayModes();

            string category = "Ekran";
            foreach (var spec in ClientConfig.Specs.Where(x => ExternalKeys.Contains(x.Key)))
            {
                if (category != spec.Category) { category = spec.Category; AddHeading(table, category); }
                Control editor;
                if (spec.Text)
                {
                    editor = new TextBox { Text = config.Values[spec.Key], MaxLength = 19, Dock = DockStyle.Fill };
                }
                else if (spec.Minimum == 0 && spec.Maximum == 1 && spec.Decimals == 0)
                {
                    var check = new CheckBox { Checked = config.Values[spec.Key] == "1", AutoSize = true, Text = config.Values[spec.Key] == "1" ? "Açık" : "Kapalı", Anchor = AnchorStyles.Left };
                    check.CheckedChanged += (s, e) => check.Text = check.Checked ? "Açık" : "Kapalı";
                    editor = check;
                }
                else
                {
                    var combo = new DarkChoice { Dock = DockStyle.Fill };
                    foreach (var value in Choices(spec)) combo.Items.Add(value);
                    var selected = combo.Items.Cast<string>().ToList().FindIndex(x => x == Normalize(config.Values[spec.Key], spec.Decimals));
                    combo.SelectedIndex = selected >= 0 ? selected : 0;
                    editor = combo;
                }
                StyleEditor(editor);
                editors[spec.Key] = editor;
                AddRow(table, spec.Label, editor);
            }
            panel.Controls.Add(table);

            var buttons = new FlowLayoutPanel { Dock = DockStyle.Bottom, Height = 58, FlowDirection = FlowDirection.RightToLeft, Padding = new Padding(10), BackColor = Color.FromArgb(29, 24, 20) };
            var save = new Button { Text = "KAYDET", Width = 110, Height = 34 };
            var cancel = new Button { Text = "İPTAL", Width = 110, Height = 34 };
            var defaults = new Button { Text = "VARSAYILANLAR", Width = 135, Height = 34 };
            StyleButton(save, true); StyleButton(cancel, false); StyleButton(defaults, false);
            save.Click += SaveClick;
            cancel.Click += (s, e) => Close();
            defaults.Click += DefaultsClick;
            buttons.Controls.Add(save); buttons.Controls.Add(cancel); buttons.Controls.Add(defaults);
            Controls.Add(panel); Controls.Add(buttons); Controls.Add(CreateTitleBar("VALIANT2 AYARLARI"));
        }

        private Panel CreateTitleBar(string caption)
        {
            var bar = new Panel { Dock = DockStyle.Top, Height = 38, BackColor = Color.FromArgb(24, 20, 17) };
            var text = new Label { Text = caption, Dock = DockStyle.Fill, ForeColor = Color.FromArgb(202, 157, 67), TextAlign = ContentAlignment.MiddleLeft, Padding = new Padding(13, 0, 0, 0), Font = new Font("Georgia", 9F, FontStyle.Bold) };
            var close = new Button { Text = "×", Dock = DockStyle.Right, Width = 44, FlatStyle = FlatStyle.Flat, BackColor = Color.FromArgb(87, 27, 24), ForeColor = Color.FromArgb(235, 214, 166), Font = new Font("Georgia", 14F) };
            var minimize = new Button { Text = "—", Dock = DockStyle.Right, Width = 44, FlatStyle = FlatStyle.Flat, BackColor = Color.FromArgb(38, 31, 26), ForeColor = Color.FromArgb(218, 193, 142), Font = new Font("Georgia", 10F) };
            close.FlatAppearance.BorderSize = 0; minimize.FlatAppearance.BorderSize = 0;
            close.Click += (s, e) => Close(); minimize.Click += (s, e) => WindowState = FormWindowState.Minimized;
            MouseEventHandler drag = (s, e) => { if (e.Button == MouseButtons.Left) { ReleaseCapture(); SendMessage(Handle, 0xA1, new IntPtr(2), IntPtr.Zero); } };
            bar.MouseDown += drag; text.MouseDown += drag;
            bar.Controls.Add(text); bar.Controls.Add(minimize); bar.Controls.Add(close);
            return bar;
        }

        private static void StyleEditor(Control control)
        {
            control.BackColor = Color.FromArgb(39, 33, 28);
            control.ForeColor = Color.FromArgb(232, 216, 180);
            control.Font = new Font("Georgia", 9F);
            var check = control as CheckBox;
            if (check != null)
            {
                check.Appearance = Appearance.Button;
                check.FlatStyle = FlatStyle.Flat;
                check.FlatAppearance.BorderColor = Color.FromArgb(145, 108, 43);
                check.FlatAppearance.CheckedBackColor = Color.FromArgb(105, 35, 31);
                check.FlatAppearance.MouseOverBackColor = Color.FromArgb(74, 50, 35);
                check.AutoSize = false; check.Width = 112; check.Height = 26; check.TextAlign = ContentAlignment.MiddleCenter;
            }
        }

        private static void StyleButton(Button button, bool primary)
        {
            button.FlatStyle = FlatStyle.Flat;
            button.FlatAppearance.BorderColor = Color.FromArgb(174, 132, 52);
            button.FlatAppearance.MouseOverBackColor = Color.FromArgb(105, 35, 31);
            button.FlatAppearance.MouseDownBackColor = Color.FromArgb(70, 22, 19);
            button.BackColor = primary ? Color.FromArgb(119, 36, 31) : Color.FromArgb(39, 33, 28);
            button.ForeColor = Color.FromArgb(235, 214, 166);
            button.Font = new Font("Georgia", 9F, FontStyle.Bold);
        }

        private static void AddHeading(TableLayoutPanel table, string text)
        {
            var label = new Label { Text = "—  " + text.ToUpperInvariant() + "  —", Font = new Font("Georgia", 11F, FontStyle.Bold), ForeColor = Color.FromArgb(210, 164, 70), AutoSize = true, Padding = new Padding(0, 15, 0, 6) };
            table.Controls.Add(label); table.SetColumnSpan(label, 2);
        }

        private static void AddRow(TableLayoutPanel table, string text, Control control)
        {
            table.Controls.Add(new Label { Text = text, AutoSize = true, Anchor = AnchorStyles.Left, ForeColor = Color.FromArgb(205, 192, 163), Padding = new Padding(0, 7, 0, 0) });
            table.Controls.Add(control);
        }

        private void LoadDisplayModes()
        {
            var dev = new DevMode();
            dev.Size = (short)Marshal.SizeOf(typeof(DevMode));
            for (var i = 0; EnumDisplaySettings(null, i, ref dev); i++)
            {
                if (dev.PelsWidth < 800 || dev.PelsHeight < 600 || (dev.BitsPerPel != 16 && dev.BitsPerPel != 32)) continue;
                if (!displayModes.Any(x => x.Width == dev.PelsWidth && x.Height == dev.PelsHeight && x.Bpp == dev.BitsPerPel && x.Frequency == dev.DisplayFrequency))
                    displayModes.Add(new DisplayMode { Width = dev.PelsWidth, Height = dev.PelsHeight, Bpp = dev.BitsPerPel, Frequency = dev.DisplayFrequency });
            }
            displayModes.Sort((a, b) => a.Width != b.Width ? a.Width.CompareTo(b.Width) : a.Height.CompareTo(b.Height));
            foreach (var size in displayModes.Select(x => x.Width + " × " + x.Height).Distinct()) screenSize.Items.Add(size);
            var currentSize = config.Values["WIDTH"] + " × " + config.Values["HEIGHT"];
            var selected = screenSize.Items.FindIndex(x => x.ToString() == currentSize);
            screenSize.SelectedIndex = selected >= 0 ? selected : 0;
            UpdateColorDepth(config.Values["BPP"], config.Values["FREQUENCY"]);
            screenSize.SelectedIndexChanged += (s, e) => { if (!updatingDisplayModes) UpdateColorDepth(null, null); };
            colorDepth.SelectedIndexChanged += (s, e) => { if (!updatingDisplayModes) UpdateRefreshRate(null); };
        }

        private void UpdateColorDepth(string preferredDepth, string preferredRate)
        {
            updatingDisplayModes = true;
            var modes = ModesForSelectedSize();
            colorDepth.Items.Clear();
            foreach (var depth in modes.Select(x => x.Bpp).Distinct().OrderBy(x => x)) colorDepth.Items.Add(depth + " bit");
            var depthIndex = colorDepth.Items.FindIndex(x => x.ToString() == preferredDepth + " bit");
            colorDepth.SelectedIndex = depthIndex >= 0 ? depthIndex : Math.Max(0, colorDepth.Items.Count - 1);
            UpdateRefreshRate(preferredRate);
            updatingDisplayModes = false;
        }

        private void UpdateRefreshRate(string preferredRate)
        {
            var modes = ModesForSelectedSize();
            var depth = colorDepth.SelectedItem == null ? 32 : int.Parse(colorDepth.SelectedItem.ToString().Split(' ')[0]);
            refreshRate.Items.Clear();
            foreach (var rate in modes.Where(x => x.Bpp == depth).Select(x => x.Frequency).Distinct().OrderBy(x => x)) refreshRate.Items.Add(rate + " Hz");
            var rateIndex = refreshRate.Items.FindIndex(x => x.ToString() == preferredRate + " Hz");
            refreshRate.SelectedIndex = rateIndex >= 0 ? rateIndex : Math.Max(0, refreshRate.Items.Count - 1);
        }

        private List<DisplayMode> ModesForSelectedSize()
        {
            if (screenSize.SelectedItem == null) return new List<DisplayMode>();
            var parts = screenSize.SelectedItem.ToString().Split('×');
            var width = int.Parse(parts[0].Trim()); var height = int.Parse(parts[1].Trim());
            return displayModes.Where(x => x.Width == width && x.Height == height).ToList();
        }

        private static IEnumerable<string> Choices(SettingSpec spec)
        {
            if (spec.Key == "ENTITY_SHOW_DISTANCE") return new[] { "2500", "4500", "6500" };
            var values = new List<string>();
            for (var value = spec.Minimum; value <= spec.Maximum; value += spec.Increment) values.Add(value.ToString("F" + spec.Decimals, CultureInfo.InvariantCulture));
            return values;
        }

        private static string Normalize(string value, int decimals)
        {
            decimal number;
            return decimal.TryParse(value, NumberStyles.Float, CultureInfo.InvariantCulture, out number) ? number.ToString("F" + decimals, CultureInfo.InvariantCulture) : value;
        }

        private void DefaultsClick(object sender, EventArgs e)
        {
            foreach (var spec in ClientConfig.Specs.Where(x => editors.ContainsKey(x.Key))) SetEditor(spec, spec.Default);
            var size = screenSize.Items.FindIndex(x => x.ToString() == "1280 × 720");
            if (size >= 0) screenSize.SelectedIndex = size;
            UpdateColorDepth("32", "60");
        }

        private void SetEditor(SettingSpec spec, string value)
        {
            var text = editors[spec.Key] as TextBox;
            if (text != null) { text.Text = value; return; }
            var check = editors[spec.Key] as CheckBox;
            if (check != null) { check.Checked = value == "1"; return; }
            var combo = (DarkChoice)editors[spec.Key];
            var index = combo.Items.Cast<string>().ToList().FindIndex(x => x == Normalize(value, spec.Decimals));
            combo.SelectedIndex = index >= 0 ? index : 0;
        }

        private void SaveClick(object sender, EventArgs e)
        {
            if (screenSize.SelectedItem == null || colorDepth.SelectedItem == null || refreshRate.SelectedItem == null) { MessageBox.Show("Geçerli ekran ayarları seçin."); return; }
            var size = screenSize.SelectedItem.ToString().Split('×');
            config.Values["WIDTH"] = size[0].Trim(); config.Values["HEIGHT"] = size[1].Trim();
            config.Values["BPP"] = colorDepth.SelectedItem.ToString().Split(' ')[0];
            config.Values["FREQUENCY"] = refreshRate.SelectedItem.ToString().Split(' ')[0];
            foreach (var spec in ClientConfig.Specs.Where(x => editors.ContainsKey(x.Key)))
            {
                var text = editors[spec.Key] as TextBox;
                var check = editors[spec.Key] as CheckBox;
                config.Values[spec.Key] = text != null ? (text.Text.Trim().Length == 0 ? "0" : text.Text.Trim()) : check != null ? (check.Checked ? "1" : "0") : ((DarkChoice)editors[spec.Key]).SelectedItem.ToString();
            }
            try { config.Save(path); MessageBox.Show("Ayarlar kaydedildi.", "VALIANT2", MessageBoxButtons.OK, MessageBoxIcon.Information); Close(); }
            catch (Exception ex) { MessageBox.Show(ex.Message, "VALIANT2", MessageBoxButtons.OK, MessageBoxIcon.Error); }
        }
    }
}
