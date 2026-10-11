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

    internal sealed class DarkChoice : Control
    {
        public readonly List<object> Items = new List<object>();
        private int selectedIndex = -1;
        public int SelectedIndex { get { return selectedIndex; } set { selectedIndex = Items.Count == 0 ? -1 : Math.Max(0, Math.Min(value, Items.Count - 1)); Invalidate(); } }
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
            TextRenderer.DrawText(e.Graphics, "‹", new Font("Georgia", 12, FontStyle.Bold), new Rectangle(Width - 33, 0, 15, Height), Color.FromArgb(218, 174, 76), TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter);
            TextRenderer.DrawText(e.Graphics, "›", new Font("Georgia", 12, FontStyle.Bold), new Rectangle(Width - 17, 0, 15, Height), Color.FromArgb(218, 174, 76), TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter);
        }

        protected override void OnMouseDown(MouseEventArgs e)
        {
            base.OnMouseDown(e); Focus();
            if (Items.Count == 0) return;
            SelectedIndex = e.X < Width - 17 ? (selectedIndex <= 0 ? Items.Count - 1 : selectedIndex - 1) : (selectedIndex + 1) % Items.Count;
        }

        protected override void OnMouseWheel(MouseEventArgs e)
        {
            if (Items.Count == 0) return;
            SelectedIndex = e.Delta > 0 ? (selectedIndex <= 0 ? Items.Count - 1 : selectedIndex - 1) : (selectedIndex + 1) % Items.Count;
        }

        protected override bool IsInputKey(Keys keyData) { return keyData == Keys.Left || keyData == Keys.Right || base.IsInputKey(keyData); }
        protected override void OnKeyDown(KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Left) OnMouseWheel(new MouseEventArgs(MouseButtons.None, 0, 0, 0, 120));
            else if (e.KeyCode == Keys.Right) OnMouseWheel(new MouseEventArgs(MouseButtons.None, 0, 0, 0, -120));
            else base.OnKeyDown(e);
        }
    }

    internal sealed class DarkScrollBar : Control
    {
        private int value, maximum, viewport, dragOffset;
        private bool dragging;
        public event EventHandler ValueChanged;
        public int Value { get { return value; } set { var next = Math.Max(0, Math.Min(value, Math.Max(0, maximum - viewport))); if (this.value == next) return; this.value = next; Invalidate(); if (ValueChanged != null) ValueChanged(this, EventArgs.Empty); } }
        public int Maximum { get { return maximum; } set { maximum = Math.Max(0, value); Value = this.value; Invalidate(); } }
        public int Viewport { get { return viewport; } set { viewport = Math.Max(1, value); Value = this.value; Invalidate(); } }

        public DarkScrollBar() { Width = 18; DoubleBuffered = true; BackColor = Color.FromArgb(20, 17, 15); }
        private Rectangle Thumb
        {
            get
            {
                var track = Math.Max(1, Height - 8); var size = maximum <= viewport ? track : Math.Max(42, track * viewport / maximum);
                var range = Math.Max(1, maximum - viewport); var top = 4 + (track - size) * value / range;
                return new Rectangle(4, top, Width - 8, size);
            }
        }
        protected override void OnPaint(PaintEventArgs e)
        {
            using (var line = new Pen(Color.FromArgb(81, 60, 31))) e.Graphics.DrawLine(line, Width / 2, 4, Width / 2, Height - 4);
            var thumb = Thumb;
            using (var fill = new SolidBrush(Color.FromArgb(105, 35, 31))) e.Graphics.FillRectangle(fill, thumb);
            using (var border = new Pen(Color.FromArgb(196, 148, 55))) e.Graphics.DrawRectangle(border, thumb.X, thumb.Y, thumb.Width - 1, thumb.Height - 1);
        }
        protected override void OnMouseDown(MouseEventArgs e)
        {
            var thumb = Thumb;
            if (thumb.Contains(e.Location)) { dragging = true; dragOffset = e.Y - thumb.Y; Capture = true; }
            else Value += e.Y < thumb.Y ? -viewport : viewport;
        }
        protected override void OnMouseMove(MouseEventArgs e)
        {
            if (!dragging) return;
            var track = Math.Max(1, Height - 8); var size = Thumb.Height; var pixels = Math.Max(1, track - size);
            Value = (e.Y - 4 - dragOffset) * Math.Max(0, maximum - viewport) / pixels;
        }
        protected override void OnMouseUp(MouseEventArgs e) { dragging = false; Capture = false; }
    }

    internal sealed class BufferedPanel : Panel
    {
        public BufferedPanel()
        {
            SetStyle(ControlStyles.AllPaintingInWmPaint | ControlStyles.UserPaint | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw, true);
            UpdateStyles();
        }
    }

    internal sealed class BufferedTable : TableLayoutPanel
    {
        public BufferedTable()
        {
            SetStyle(ControlStyles.AllPaintingInWmPaint | ControlStyles.UserPaint | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw, true);
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

        private readonly string path;
        private readonly ClientConfig config;
        private readonly Dictionary<string, Control> editors = new Dictionary<string, Control>(StringComparer.OrdinalIgnoreCase);
        private readonly DarkChoice resolution = new DarkChoice { Dock = DockStyle.Fill };

        protected override CreateParams CreateParams
        {
            get
            {
                var parameters = base.CreateParams;
                parameters.ExStyle |= 0x02000000;
                return parameters;
            }
        }

        public ConfigForm(string path)
        {
            this.path = path;
            config = ClientConfig.Load(path);
            Text = "VALIANT2 Ayarları";
            StartPosition = FormStartPosition.CenterScreen;
            FormBorderStyle = FormBorderStyle.None;
            Padding = new Padding(2);
            MinimumSize = new Size(680, 620);
            Size = new Size(780, 840);
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
            var scroll = new DarkScrollBar { Dock = DockStyle.Right };
            var table = new BufferedTable { AutoSize = true, AutoSizeMode = AutoSizeMode.GrowAndShrink, ColumnCount = 2, Width = ClientSize.Width - 32, Padding = new Padding(22), BackColor = Color.FromArgb(18, 16, 14), ForeColor = Color.FromArgb(218, 204, 170) };
            table.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 58));
            table.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 42));
            AddHeading(table, "Ekran");
            StyleEditor(resolution);
            AddRow(table, "Çözünürlük", resolution);
            LoadDisplayModes();

            string category = null;
            foreach (var spec in ClientConfig.Specs.Where(x => !new[] { "WIDTH", "HEIGHT", "BPP", "FREQUENCY" }.Contains(x.Key)))
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
            panel.Controls.Add(scroll);
            Action syncScroll = () => { scroll.Maximum = table.Height; scroll.Viewport = panel.ClientSize.Height; table.Top = -scroll.Value; table.Width = Math.Max(300, panel.ClientSize.Width - scroll.Width); };
            scroll.ValueChanged += (s, e) => table.Top = -scroll.Value;
            panel.Resize += (s, e) => syncScroll();
            table.SizeChanged += (s, e) => syncScroll();
            panel.MouseWheel += (s, e) => scroll.Value -= e.Delta / 6;

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
            var modes = new List<DisplayMode>();
            var dev = new DevMode();
            dev.Size = (short)Marshal.SizeOf(typeof(DevMode));
            for (var i = 0; EnumDisplaySettings(null, i, ref dev); i++)
            {
                if (dev.PelsWidth < 800 || dev.PelsHeight < 600 || (dev.BitsPerPel != 16 && dev.BitsPerPel != 32)) continue;
                if (!modes.Any(x => x.Width == dev.PelsWidth && x.Height == dev.PelsHeight && x.Bpp == dev.BitsPerPel && x.Frequency == dev.DisplayFrequency))
                    modes.Add(new DisplayMode { Width = dev.PelsWidth, Height = dev.PelsHeight, Bpp = dev.BitsPerPel, Frequency = dev.DisplayFrequency });
            }
            modes = modes.OrderBy(x => x.Width).ThenBy(x => x.Height).ThenBy(x => x.Bpp).ThenBy(x => x.Frequency).ToList();
            foreach (var mode in modes) resolution.Items.Add(mode);
            var selected = modes.FindIndex(x => x.Width.ToString() == config.Values["WIDTH"] && x.Height.ToString() == config.Values["HEIGHT"] && x.Bpp.ToString() == config.Values["BPP"] && x.Frequency.ToString() == config.Values["FREQUENCY"]);
            if (selected < 0) selected = modes.FindIndex(x => x.Width.ToString() == config.Values["WIDTH"] && x.Height.ToString() == config.Values["HEIGHT"] && x.Bpp.ToString() == config.Values["BPP"]);
            if (resolution.Items.Count > 0) resolution.SelectedIndex = selected >= 0 ? selected : 0;
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
            var mode = resolution.Items.Cast<DisplayMode>().ToList().FindIndex(x => x.Width == 1280 && x.Height == 720 && x.Bpp == 32);
            if (mode >= 0) resolution.SelectedIndex = mode;
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
            var mode = resolution.SelectedItem as DisplayMode;
            if (mode == null) { MessageBox.Show("Geçerli bir çözünürlük seçin."); return; }
            config.Values["WIDTH"] = mode.Width.ToString(); config.Values["HEIGHT"] = mode.Height.ToString();
            config.Values["BPP"] = mode.Bpp.ToString(); config.Values["FREQUENCY"] = mode.Frequency.ToString();
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
