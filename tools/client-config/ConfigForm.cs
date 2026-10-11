using System;
using System.Collections.Generic;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Linq;
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
            new SettingSpec("WINDOWED", "Pencere modu (0/1)", "Ekran", "0", 0, 1),
            new SettingSpec("GAMMA", "Gamma", "Ekran", "5", 1, 5),
            new SettingSpec("FIELD_OF_VIEW_RATE", "Görüş alanı oranı", "Ekran", "0.00", -1, 1, 0.05m, 2),
            new SettingSpec("MUSIC_VOLUME", "Müzik sesi", "Ses", "1.000", 0, 1, 0.05m, 3),
            new SettingSpec("VOICE_VOLUME", "Efekt sesi", "Ses", "5", 0, 5),
            new SettingSpec("SOFTWARE_CURSOR", "Yazılımsal imleç (0/1)", "Temel", "0", 0, 1),
            new SettingSpec("OBJECT_CULLING", "Nesne ayıklama (0/1)", "Temel", "1", 0, 1),
            new SettingSpec("VISIBILITY", "Görüş mesafesi seviyesi", "Temel", "3", 0, 5),
            new SettingSpec("USE_DEFAULT_IME", "Sistem IME (0/1)", "Temel", "0", 0, 1),
            new SettingSpec("SOFTWARE_TILING", "Yazılımsal döşeme", "Temel", "0", 0, 2),
            new SettingSpec("DECOMPRESSED_TEXTURE", "Açılmış dokular (0/1)", "Temel", "0", 0, 1),
            new SettingSpec("IS_SAVE_ID", "Kullanıcı adını kaydet (0/1)", "Temel", "0", 0, 1),
            new SettingSpec("SAVE_ID", "Kayıtlı kullanıcı adı", "Temel", "0"),
            new SettingSpec("SHADOW_LEVEL", "Gölge seviyesi", "Grafik", "5", 0, 5),
            new SettingSpec("TEXT_OUTLINE", "İsim kenarlığı (0/1)", "Grafik", "1", 0, 1),
            new SettingSpec("AFFECT_ICONS", "Etki simgeleri (0/1)", "Grafik", "1", 0, 1),
            new SettingSpec("HIGHLIGHT_ANIMATION", "Vurgu animasyonu (0/1)", "Grafik", "1", 0, 1),
            new SettingSpec("HIDE_EFFECTS", "Efektleri gizle (0/1)", "Grafik", "0", 0, 1),
            new SettingSpec("HIDE_TOOLTIP_EMOJIS", "Emoji ipuçlarını gizle (0/1)", "Grafik", "1", 0, 1),
            new SettingSpec("METINSTONE_SCALE_RATE", "Metin taşı ölçeği", "Grafik", "0.0", 0, 1, 0.1m, 1),
            new SettingSpec("DAMAGE_TEXTURE_SCALE_RATE", "Hasar yazısı ölçeği", "Grafik", "0.0", 0, 1, 0.1m, 1),
            new SettingSpec("SELECTED_SKYBOX_TYPE", "Gökyüzü tipi", "Grafik", "0", 0, 20),
            new SettingSpec("ANIMATION_TYPE", "Animasyon tipi", "Grafik", "5", 0, 20),
            new SettingSpec("FONT_TYPE", "Yazı tipi", "Grafik", "0", 0, 20),
            new SettingSpec("ENTITY_SHOW_DISTANCE", "Varlık mesafesi", "Optimizasyon", "6500", 2500, 6500, 2000),
            new SettingSpec("MAP_LOADING_DISTANCE", "Harita yükleme mesafesi", "Optimizasyon", "0.0", 0, 10000, 100, 1),
            new SettingSpec("HIDE_PETS", "Petleri gizle (0/1)", "Gizleme", "0", 0, 1),
            new SettingSpec("HIDE_MOUNTS", "Binekleri gizle (0/1)", "Gizleme", "0", 0, 1),
            new SettingSpec("HIDE_SHOPS", "Pazarları gizle (0/1)", "Gizleme", "0", 0, 1),
            new SettingSpec("HIDE_NPC", "NPC'leri gizle (0/1)", "Gizleme", "0", 0, 1),
            new SettingSpec("VIEW_CHAT", "Sohbeti göster (0/1)", "Arayüz", "1", 0, 1),
            new SettingSpec("ALWAYS_VIEW_NAME", "İsimleri göster (0/1)", "Arayüz", "1", 0, 1),
            new SettingSpec("SHOW_DAMAGE", "Hasarı göster (0/1)", "Arayüz", "1", 0, 1),
            new SettingSpec("SHOW_SALESTEXT", "Pazar yazılarını göster (0/1)", "Arayüz", "1", 0, 1),
            new SettingSpec("SHOW_MOBAIFLAG", "Canavar tipini göster (0/1)", "Arayüz", "1", 0, 1),
            new SettingSpec("SHOW_MOBLEVEL", "Canavar seviyesini göster (0/1)", "Arayüz", "1", 0, 1),
            new SettingSpec("DAMAGE_TYPE", "Hasar tipi", "Arayüz", "0", 0, 20),
            new SettingSpec("DAMAGE_TYPE_RENEWED", "Yeni hasar görünümü (0/1)", "Arayüz", "0", 0, 1),
            new SettingSpec("HIDE_EVENT_IMAGE", "Etkinlik görselini gizle (0/1)", "Arayüz", "1", 0, 1),
            new SettingSpec("ANIMATED_LOADING", "Animasyonlu yükleme (0/1)", "Arayüz", "1", 0, 1)
        };

        public readonly Dictionary<string, string> Values = Specs.ToDictionary(x => x.Key, x => x.Default, StringComparer.OrdinalIgnoreCase);
        private readonly Dictionary<string, string> unknown = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);

        public static ClientConfig Load(string path)
        {
            var config = new ClientConfig();
            if (!File.Exists(path)) return config;
            foreach (var raw in File.ReadAllLines(path))
            {
                var line = raw.Trim();
                if (line.Length == 0) continue;
                var parts = line.Split((char[])null, 2, StringSplitOptions.RemoveEmptyEntries);
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

    internal sealed class ConfigForm : Form
    {
        private readonly string path;
        private readonly ClientConfig config;
        private readonly Dictionary<string, Control> editors = new Dictionary<string, Control>(StringComparer.OrdinalIgnoreCase);

        public ConfigForm(string path)
        {
            this.path = path;
            config = ClientConfig.Load(path);
            Text = "VALIANT2 Ayarları";
            StartPosition = FormStartPosition.CenterScreen;
            MinimumSize = new Size(560, 560);
            Size = new Size(680, 720);
            BuildInterface();
        }

        private void BuildInterface()
        {
            var tabs = new TabControl { Dock = DockStyle.Fill };
            foreach (var category in ClientConfig.Specs.Select(x => x.Category).Distinct())
            {
                var page = new TabPage(category) { AutoScroll = true };
                var table = new TableLayoutPanel { AutoSize = true, AutoSizeMode = AutoSizeMode.GrowAndShrink, ColumnCount = 2, Dock = DockStyle.Top, Padding = new Padding(12) };
                table.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 62));
                table.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 38));
                foreach (var spec in ClientConfig.Specs.Where(x => x.Category == category))
                {
                    var label = new Label { Text = spec.Label, AutoSize = true, Anchor = AnchorStyles.Left, Padding = new Padding(0, 7, 0, 0) };
                    Control editor;
                    if (spec.Text)
                    {
                        editor = new TextBox { Text = config.Values[spec.Key], MaxLength = 19, Dock = DockStyle.Fill };
                    }
                    else
                    {
                        decimal value;
                        decimal.TryParse(config.Values[spec.Key], NumberStyles.Float, CultureInfo.InvariantCulture, out value);
                        var numeric = new NumericUpDown { Minimum = spec.Minimum, Maximum = spec.Maximum, Increment = spec.Increment, DecimalPlaces = spec.Decimals, Dock = DockStyle.Fill, ThousandsSeparator = false };
                        numeric.Value = Math.Min(spec.Maximum, Math.Max(spec.Minimum, value));
                        editor = numeric;
                    }
                    editor.Tag = spec;
                    editors[spec.Key] = editor;
                    table.Controls.Add(label);
                    table.Controls.Add(editor);
                }
                page.Controls.Add(table);
                tabs.TabPages.Add(page);
            }

            var buttons = new FlowLayoutPanel { Dock = DockStyle.Bottom, Height = 48, FlowDirection = FlowDirection.RightToLeft, Padding = new Padding(8) };
            var save = new Button { Text = "Kaydet", Width = 100 };
            var cancel = new Button { Text = "İptal", Width = 100 };
            var defaults = new Button { Text = "Varsayılanlar", Width = 110 };
            save.Click += SaveClick;
            cancel.Click += (s, e) => Close();
            defaults.Click += DefaultsClick;
            buttons.Controls.Add(save);
            buttons.Controls.Add(cancel);
            buttons.Controls.Add(defaults);
            Controls.Add(tabs);
            Controls.Add(buttons);
        }

        private void DefaultsClick(object sender, EventArgs e)
        {
            foreach (var spec in ClientConfig.Specs) SetEditorValue(spec, spec.Default);
        }

        private void SetEditorValue(SettingSpec spec, string value)
        {
            var text = editors[spec.Key] as TextBox;
            if (text != null) { text.Text = value; return; }
            decimal number;
            decimal.TryParse(value, NumberStyles.Float, CultureInfo.InvariantCulture, out number);
            ((NumericUpDown)editors[spec.Key]).Value = Math.Min(spec.Maximum, Math.Max(spec.Minimum, number));
        }

        private void SaveClick(object sender, EventArgs e)
        {
            foreach (var spec in ClientConfig.Specs)
            {
                var text = editors[spec.Key] as TextBox;
                config.Values[spec.Key] = text != null ? (text.Text.Trim().Length == 0 ? "0" : text.Text.Trim()) : ((NumericUpDown)editors[spec.Key]).Value.ToString("F" + spec.Decimals, CultureInfo.InvariantCulture);
            }
            try
            {
                config.Save(path);
                MessageBox.Show("Ayarlar kaydedildi.", "VALIANT2", MessageBoxButtons.OK, MessageBoxIcon.Information);
                Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "VALIANT2", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
