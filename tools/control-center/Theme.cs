using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Runtime.InteropServices;
using System.Windows.Forms;

namespace Valiant2ControlCenter
{
    internal static class Theme
    {
        public static readonly Color BgDark       = Color.FromArgb(12, 10, 8);
        public static readonly Color BgMain       = Color.FromArgb(18, 14, 11);
        public static readonly Color BgSidebar    = Color.FromArgb(15, 12, 9);
        public static readonly Color BgCard       = Color.FromArgb(25, 20, 15);
        public static readonly Color BgInput      = Color.FromArgb(14, 11, 9);
        public static readonly Color BgConsole    = Color.FromArgb(10, 8, 6);

        public static readonly Color Gold         = Color.FromArgb(198, 156, 78);
        public static readonly Color GoldBright   = Color.FromArgb(236, 202, 128);
        public static readonly Color GoldDim      = Color.FromArgb(118, 90, 44);
        public static readonly Color BorderDark   = Color.FromArgb(58, 45, 28);
        public static readonly Color BorderGold   = Color.FromArgb(146, 112, 54);

        public static readonly Color Crimson      = Color.FromArgb(128, 30, 26);
        public static readonly Color CrimsonHover = Color.FromArgb(162, 42, 36);
        public static readonly Color Emerald      = Color.FromArgb(46, 164, 92);
        public static readonly Color EmeraldBg    = Color.FromArgb(20, 52, 32);
        public static readonly Color Amber        = Color.FromArgb(218, 158, 44);
        public static readonly Color AmberBg      = Color.FromArgb(62, 46, 18);
        public static readonly Color Danger       = Color.FromArgb(216, 68, 62);
        public static readonly Color DangerBg     = Color.FromArgb(64, 20, 20);

        public static readonly Color TextMain     = Color.FromArgb(226, 212, 184);
        public static readonly Color TextMuted    = Color.FromArgb(148, 132, 104);

        public static readonly Font FontTitle     = new Font("Georgia", 14F, FontStyle.Bold, GraphicsUnit.Pixel);
        public static readonly Font FontSubtitle  = new Font("Georgia", 12.5F, FontStyle.Bold, GraphicsUnit.Pixel);
        public static readonly Font FontCardTitle = new Font("Georgia", 11.5F, FontStyle.Bold, GraphicsUnit.Pixel);
        public static readonly Font FontNav       = new Font("Georgia", 11.5F, FontStyle.Bold, GraphicsUnit.Pixel);
        public static readonly Font FontButton    = new Font("Georgia", 11F, FontStyle.Bold, GraphicsUnit.Pixel);
        public static readonly Font FontButtonSm  = new Font("Georgia", 10F, FontStyle.Bold, GraphicsUnit.Pixel);
        public static readonly Font FontBody      = new Font("Segoe UI", 11.5F, FontStyle.Regular, GraphicsUnit.Pixel);
        public static readonly Font FontBodyBold  = new Font("Segoe UI", 11.5F, FontStyle.Bold, GraphicsUnit.Pixel);
        public static readonly Font FontSmall     = new Font("Segoe UI", 10.5F, FontStyle.Regular, GraphicsUnit.Pixel);
        public static readonly Font FontMono      = new Font("Consolas", 11F, FontStyle.Regular, GraphicsUnit.Pixel);

        public static void DisableMnemonicsRecursive(Control root)
        {
            if (root == null) return;
            var lbl = root as Label;
            if (lbl != null) lbl.UseMnemonic = false;
            var btn = root as ButtonBase;
            if (btn != null) btn.UseMnemonic = false;
            foreach (Control child in root.Controls)
                DisableMnemonicsRecursive(child);
        }

        public static void DrawOrnateBorder(Graphics g, Rectangle rect, bool highlight = false)
        {
            if (rect.Width <= 4 || rect.Height <= 4) return;
            using (var outerPen = new Pen(highlight ? Gold : BorderDark, 1))
            using (var innerPen = new Pen(highlight ? BorderGold : Color.FromArgb(36, 28, 19), 1))
            using (var cornerPen = new Pen(highlight ? GoldBright : GoldDim, 2))
            {
                g.DrawRectangle(outerPen, rect.X, rect.Y, rect.Width - 1, rect.Height - 1);
                g.DrawRectangle(innerPen, rect.X + 2, rect.Y + 2, rect.Width - 5, rect.Height - 5);

                int c = 6;
                g.DrawLine(cornerPen, rect.X, rect.Y, rect.X + c, rect.Y);
                g.DrawLine(cornerPen, rect.X, rect.Y, rect.X, rect.Y + c);
                g.DrawLine(cornerPen, rect.Right - 1 - c, rect.Y, rect.Right - 1, rect.Y);
                g.DrawLine(cornerPen, rect.Right - 1, rect.Y, rect.Right - 1, rect.Y + c);
                g.DrawLine(cornerPen, rect.X, rect.Bottom - 1 - c, rect.X, rect.Bottom - 1);
                g.DrawLine(cornerPen, rect.X, rect.Bottom - 1, rect.X + c, rect.Bottom - 1);
                g.DrawLine(cornerPen, rect.Right - 1 - c, rect.Bottom - 1, rect.Right - 1, rect.Bottom - 1);
                g.DrawLine(cornerPen, rect.Right - 1, rect.Bottom - 1 - c, rect.Right - 1, rect.Bottom - 1);
            }
        }

        public static Button CreateButton(string text, ButtonStyle style = ButtonStyle.Secondary, int width = 120, int height = 28)
        {
            var btn = new Button
            {
                Text = text,
                Size = new Size(width, height),
                FlatStyle = FlatStyle.Flat,
                Cursor = Cursors.Hand,
                Font = FontButton,
                UseVisualStyleBackColor = false,
                UseMnemonic = false
            };
            ApplyButtonStyle(btn, style);
            return btn;
        }

        public static void ApplyButtonStyle(Button btn, ButtonStyle style)
        {
            btn.FlatAppearance.BorderSize = 1;
            switch (style)
            {
                case ButtonStyle.PrimaryCrimson:
                    btn.BackColor = Crimson;
                    btn.ForeColor = GoldBright;
                    btn.FlatAppearance.BorderColor = Gold;
                    btn.FlatAppearance.MouseOverBackColor = CrimsonHover;
                    btn.FlatAppearance.MouseDownBackColor = Color.FromArgb(95, 20, 18);
                    break;
                case ButtonStyle.PrimaryGold:
                    btn.BackColor = Color.FromArgb(78, 58, 28);
                    btn.ForeColor = GoldBright;
                    btn.FlatAppearance.BorderColor = GoldBright;
                    btn.FlatAppearance.MouseOverBackColor = Color.FromArgb(108, 82, 38);
                    btn.FlatAppearance.MouseDownBackColor = Color.FromArgb(62, 46, 22);
                    break;
                case ButtonStyle.Success:
                    btn.BackColor = EmeraldBg;
                    btn.ForeColor = Color.FromArgb(130, 238, 168);
                    btn.FlatAppearance.BorderColor = Emerald;
                    btn.FlatAppearance.MouseOverBackColor = Color.FromArgb(32, 82, 50);
                    btn.FlatAppearance.MouseDownBackColor = Color.FromArgb(18, 44, 28);
                    break;
                case ButtonStyle.Danger:
                    btn.BackColor = DangerBg;
                    btn.ForeColor = Color.FromArgb(255, 168, 162);
                    btn.FlatAppearance.BorderColor = Danger;
                    btn.FlatAppearance.MouseOverBackColor = Color.FromArgb(98, 32, 32);
                    btn.FlatAppearance.MouseDownBackColor = Color.FromArgb(52, 16, 16);
                    break;
                default:
                    btn.BackColor = Color.FromArgb(36, 28, 20);
                    btn.ForeColor = TextMain;
                    btn.FlatAppearance.BorderColor = BorderGold;
                    btn.FlatAppearance.MouseOverBackColor = Color.FromArgb(56, 43, 30);
                    btn.FlatAppearance.MouseDownBackColor = Color.FromArgb(28, 22, 16);
                    break;
            }
        }

        public static TextBox CreateTextBox(string initialText = "", bool readOnly = false, bool password = false)
        {
            return new TextBox
            {
                Text = initialText,
                ReadOnly = readOnly,
                UseSystemPasswordChar = password,
                BackColor = BgInput,
                ForeColor = TextMain,
                BorderStyle = BorderStyle.FixedSingle,
                Font = FontBody
            };
        }

        public static DataGridView CreateGrid()
        {
            var grid = new DataGridView
            {
                BackgroundColor = BgInput,
                BorderStyle = BorderStyle.None,
                CellBorderStyle = DataGridViewCellBorderStyle.SingleHorizontal,
                GridColor = Color.FromArgb(42, 33, 24),
                EnableHeadersVisualStyles = false,
                ColumnHeadersBorderStyle = DataGridViewHeaderBorderStyle.Single,
                ColumnHeadersHeight = 24,
                RowHeadersVisible = false,
                AllowUserToAddRows = false,
                AllowUserToDeleteRows = false,
                AllowUserToResizeRows = false,
                ReadOnly = true,
                SelectionMode = DataGridViewSelectionMode.FullRowSelect,
                MultiSelect = false,
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill,
                ScrollBars = ScrollBars.None,
                Font = FontSmall
            };
            grid.ColumnHeadersDefaultCellStyle.BackColor = Color.FromArgb(34, 26, 18);
            grid.ColumnHeadersDefaultCellStyle.ForeColor = GoldBright;
            grid.ColumnHeadersDefaultCellStyle.Font = FontBodyBold;
            grid.ColumnHeadersDefaultCellStyle.SelectionBackColor = Color.FromArgb(34, 26, 18);
            grid.DefaultCellStyle.BackColor = BgCard;
            grid.DefaultCellStyle.ForeColor = TextMain;
            grid.DefaultCellStyle.SelectionBackColor = Color.FromArgb(76, 56, 30);
            grid.DefaultCellStyle.SelectionForeColor = GoldBright;
            grid.AlternatingRowsDefaultCellStyle.BackColor = Color.FromArgb(20, 16, 12);
            grid.RowTemplate.Height = 22;

            typeof(DataGridView).InvokeMember("DoubleBuffered",
                System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.SetProperty,
                null, grid, new object[] { true });
            return grid;
        }

        public static MetinScrollBar AttachGridScrollBar(DataGridView grid, Control container)
        {
            var sb = new MetinScrollBar { Dock = DockStyle.Right };
            bool syncing = false;

            Action syncFromGrid = () =>
            {
                if (syncing || grid.IsDisposed) return;
                syncing = true;
                try
                {
                    int total = grid.RowCount;
                    int visible = Math.Max(1, grid.DisplayedRowCount(false));
                    int first = (total > 0 && grid.FirstDisplayedScrollingRowIndex >= 0) ? grid.FirstDisplayedScrollingRowIndex : 0;
                    sb.SetMetrics(total, visible, first);
                }
                catch { }
                finally { syncing = false; }
            };

            sb.ValueChanged += (s, e) =>
            {
                if (syncing || grid.IsDisposed || grid.RowCount == 0) return;
                syncing = true;
                try
                {
                    int idx = Math.Max(0, Math.Min(grid.RowCount - 1, sb.Value));
                    grid.FirstDisplayedScrollingRowIndex = idx;
                }
                catch { }
                finally { syncing = false; }
            };

            grid.MouseWheel += (s, e) =>
            {
                if (grid.RowCount == 0) return;
                int delta = e.Delta > 0 ? -3 : 3;
                int cur = grid.FirstDisplayedScrollingRowIndex >= 0 ? grid.FirstDisplayedScrollingRowIndex : 0;
                int maxFirst = Math.Max(0, grid.RowCount - Math.Max(1, grid.DisplayedRowCount(false)));
                int next = Math.Max(0, Math.Min(maxFirst, cur + delta));
                try { grid.FirstDisplayedScrollingRowIndex = next; } catch { }
                syncFromGrid();
            };

            grid.RowsAdded += (s, e) => syncFromGrid();
            grid.RowsRemoved += (s, e) => syncFromGrid();
            grid.Resize += (s, e) => syncFromGrid();
            grid.Scroll += (s, e) => syncFromGrid();
            container.Controls.Add(sb);
            return sb;
        }

        [DllImport("user32.dll")]
        private static extern int SendMessage(IntPtr hWnd, int msg, int wParam, int lParam);

        public static MetinScrollBar AttachRichTextScrollBar(RichTextBox rtb, Control container)
        {
            rtb.ScrollBars = RichTextBoxScrollBars.None;
            var sb = new MetinScrollBar { Dock = DockStyle.Right };
            bool syncing = false;

            Action syncFromBox = () =>
            {
                if (syncing || rtb.IsDisposed || !rtb.IsHandleCreated) return;
                syncing = true;
                try
                {
                    int totalLines = Math.Max(1, SendMessage(rtb.Handle, 0x00BA, 0, 0)); // EM_GETLINECOUNT
                    int firstLine = Math.Max(0, SendMessage(rtb.Handle, 0x00CE, 0, 0));  // EM_GETFIRSTVISIBLELINE
                    int visibleLines = Math.Max(1, rtb.ClientSize.Height / Math.Max(12, rtb.Font.Height));
                    sb.SetMetrics(totalLines, visibleLines, firstLine);
                }
                catch { }
                finally { syncing = false; }
            };

            sb.ValueChanged += (s, e) =>
            {
                if (syncing || rtb.IsDisposed || !rtb.IsHandleCreated) return;
                syncing = true;
                try
                {
                    int curFirst = Math.Max(0, SendMessage(rtb.Handle, 0x00CE, 0, 0));
                    int diff = sb.Value - curFirst;
                    if (diff != 0)
                        SendMessage(rtb.Handle, 0x00B6, 0, diff); // EM_LINESCROLL
                }
                catch { }
                finally { syncing = false; }
            };

            rtb.MouseWheel += (s, e) =>
            {
                if (!rtb.IsHandleCreated) return;
                int lines = e.Delta > 0 ? -3 : 3;
                SendMessage(rtb.Handle, 0x00B6, 0, lines);
                syncFromBox();
            };

            rtb.TextChanged += (s, e) => syncFromBox();
            rtb.VScroll += (s, e) => syncFromBox();
            rtb.Resize += (s, e) => syncFromBox();
            container.Controls.Add(sb);
            return sb;
        }
    }

    internal sealed class MetinScrollBar : Control
    {
        private int totalItems = 1;
        private int visibleItems = 1;
        private int currentValue = 0;
        private bool isHovered = false;
        private bool isDragging = false;
        private int dragOffsetY = 0;

        public event EventHandler ValueChanged;

        public int Value
        {
            get { return currentValue; }
            set
            {
                int maxVal = Math.Max(0, totalItems - visibleItems);
                int clamped = Math.Max(0, Math.Min(maxVal, value));
                if (currentValue != clamped)
                {
                    currentValue = clamped;
                    Invalidate();
                    var h = ValueChanged;
                    if (h != null) h(this, EventArgs.Empty);
                }
            }
        }

        public MetinScrollBar()
        {
            Width = 11;
            BackColor = Color.FromArgb(14, 11, 8);
            Cursor = Cursors.Hand;
            DoubleBuffered = true;
            SetStyle(ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw | ControlStyles.UserPaint, true);
        }

        public void SetMetrics(int total, int visible, int first)
        {
            totalItems = Math.Max(1, total);
            visibleItems = Math.Max(1, visible);
            int maxVal = Math.Max(0, totalItems - visibleItems);
            currentValue = Math.Max(0, Math.Min(maxVal, first));
            Invalidate();
        }

        private Rectangle GetThumbRect()
        {
            int trackH = Math.Max(10, Height - 4);
            if (totalItems <= visibleItems)
                return new Rectangle(2, 2, Width - 4, trackH);

            int thumbH = Math.Max(24, (int)((double)trackH * visibleItems / totalItems));
            int maxVal = Math.Max(1, totalItems - visibleItems);
            int availH = Math.Max(1, trackH - thumbH);
            int thumbY = 2 + (int)((double)availH * currentValue / maxVal);
            return new Rectangle(2, thumbY, Width - 4, thumbH);
        }

        protected override void OnMouseEnter(EventArgs e) { base.OnMouseEnter(e); isHovered = true; Invalidate(); }
        protected override void OnMouseLeave(EventArgs e) { base.OnMouseLeave(e); isHovered = false; Invalidate(); }

        protected override void OnMouseDown(MouseEventArgs e)
        {
            base.OnMouseDown(e);
            if (e.Button != MouseButtons.Left || totalItems <= visibleItems) return;
            var thumb = GetThumbRect();
            if (thumb.Contains(e.Location))
            {
                isDragging = true;
                dragOffsetY = e.Y - thumb.Y;
                Invalidate();
            }
            else
            {
                int trackH = Math.Max(10, Height - 4);
                int thumbH = thumb.Height;
                int availH = Math.Max(1, trackH - thumbH);
                int targetY = e.Y - 2 - (thumbH / 2);
                int maxVal = Math.Max(1, totalItems - visibleItems);
                Value = (int)Math.Round((double)targetY * maxVal / availH);
            }
        }

        protected override void OnMouseMove(MouseEventArgs e)
        {
            base.OnMouseMove(e);
            if (!isDragging || totalItems <= visibleItems) return;
            var thumb = GetThumbRect();
            int trackH = Math.Max(10, Height - 4);
            int availH = Math.Max(1, trackH - thumb.Height);
            int targetY = e.Y - dragOffsetY - 2;
            int maxVal = Math.Max(1, totalItems - visibleItems);
            Value = (int)Math.Round((double)targetY * maxVal / availH);
        }

        protected override void OnMouseUp(MouseEventArgs e)
        {
            base.OnMouseUp(e);
            if (isDragging) { isDragging = false; Invalidate(); }
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            var g = e.Graphics;
            using (var trackBr = new SolidBrush(Color.FromArgb(14, 11, 8)))
                g.FillRectangle(trackBr, ClientRectangle);
            using (var borderPen = new Pen(Theme.BorderDark, 1))
                g.DrawRectangle(borderPen, 0, 0, Width - 1, Height - 1);

            var thumb = GetThumbRect();
            if (thumb.Height <= 0 || thumb.Width <= 0) return;

            bool active = totalItems > visibleItems;
            Color cTop = !active
                ? Color.FromArgb(40, 32, 22)
                : (isDragging || isHovered ? Theme.GoldBright : Theme.Gold);
            Color cBot = !active
                ? Color.FromArgb(28, 22, 15)
                : (isDragging || isHovered ? Theme.Gold : Color.FromArgb(128, 94, 42));

            using (var br = new LinearGradientBrush(thumb, cTop, cBot, LinearGradientMode.Vertical))
                g.FillRectangle(br, thumb);
            using (var pen = new Pen(active ? Theme.GoldBright : Theme.BorderDark, 1))
                g.DrawRectangle(pen, thumb.X, thumb.Y, thumb.Width - 1, thumb.Height - 1);
        }
    }

    internal enum ButtonStyle
    {
        Secondary,
        PrimaryCrimson,
        PrimaryGold,
        Success,
        Danger
    }

    internal class BufferedPanel : Panel
    {
        public bool DrawCardBorder { get; set; }
        public bool HighlightBorder { get; set; }

        public BufferedPanel()
        {
            DoubleBuffered = true;
            SetStyle(ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw | ControlStyles.UserPaint, true);
            UpdateStyles();
        }

        protected override void OnControlAdded(ControlEventArgs e)
        {
            base.OnControlAdded(e);
            Theme.DisableMnemonicsRecursive(e.Control);
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            if (DrawCardBorder)
                Theme.DrawOrnateBorder(e.Graphics, ClientRectangle, HighlightBorder);
        }
    }

    internal sealed class TopTabButton : Control
    {
        private bool isSelected;
        private bool isHovered;

        public bool IsSelected
        {
            get { return isSelected; }
            set { if (isSelected != value) { isSelected = value; Invalidate(); } }
        }

        public TopTabButton(string title)
        {
            Text = title;
            Height = 34;
            Cursor = Cursors.Hand;
            DoubleBuffered = true;
            SetStyle(ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw | ControlStyles.UserPaint, true);
        }

        protected override void OnMouseEnter(EventArgs e) { base.OnMouseEnter(e); isHovered = true; Invalidate(); }
        protected override void OnMouseLeave(EventArgs e) { base.OnMouseLeave(e); isHovered = false; Invalidate(); }

        protected override void OnPaint(PaintEventArgs e)
        {
            var g = e.Graphics;
            Color bg = isSelected
                ? Color.FromArgb(56, 40, 24)
                : (isHovered ? Color.FromArgb(32, 24, 17) : Color.FromArgb(18, 14, 10));

            using (var br = new SolidBrush(bg))
                g.FillRectangle(br, ClientRectangle);

            using (var border = new Pen(isSelected ? Theme.Gold : Theme.BorderDark, 1))
                g.DrawRectangle(border, 0, 0, Width - 1, Height - 1);

            if (isSelected)
            {
                using (var accent = new SolidBrush(Theme.GoldBright))
                    g.FillRectangle(accent, 2, Height - 3, Width - 4, 2);
            }

            TextRenderer.DrawText(g, Text, Theme.FontNav, ClientRectangle,
                isSelected ? Theme.GoldBright : Theme.TextMain,
                TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter | TextFormatFlags.NoPrefix);
        }
    }

    internal sealed class MiniServicePill : BufferedPanel
    {
        public string ServiceName { get; set; }
        public bool IsOnline { get; set; }
        public bool IsWarning { get; set; }

        public MiniServicePill(string name)
        {
            ServiceName = name;
            Size = new Size(125, 25);
            Margin = new Padding(2);
            BackColor = Theme.BgCard;
        }

        public void UpdateState(bool online, bool warning = false)
        {
            if (IsOnline == online && IsWarning == warning) return;
            IsOnline = online;
            IsWarning = warning;
            Invalidate();
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            var g = e.Graphics;
            g.SmoothingMode = SmoothingMode.AntiAlias;
            Color dotColor = IsOnline ? Theme.Emerald : (IsWarning ? Theme.Amber : Theme.Danger);
            Color bg       = IsOnline ? Color.FromArgb(18, 38, 25) : (IsWarning ? Theme.AmberBg : Color.FromArgb(38, 18, 18));

            using (var br = new SolidBrush(bg))
                g.FillRectangle(br, ClientRectangle);
            using (var pen = new Pen(IsOnline ? Color.FromArgb(46, 110, 68) : Theme.BorderDark, 1))
                g.DrawRectangle(pen, 0, 0, Width - 1, Height - 1);

            using (var dotBr = new SolidBrush(dotColor))
                g.FillEllipse(dotBr, 7, 8, 8, 8);

            TextRenderer.DrawText(g, ServiceName, Theme.FontSmall,
                new Rectangle(19, 0, Width - 22, Height),
                IsOnline ? Color.FromArgb(195, 245, 210) : Theme.TextMuted,
                TextFormatFlags.Left | TextFormatFlags.VerticalCenter | TextFormatFlags.EndEllipsis | TextFormatFlags.NoPrefix);
        }
    }
}
