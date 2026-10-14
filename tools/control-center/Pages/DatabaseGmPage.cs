using System;
using System.Drawing;
using System.IO;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Valiant2ControlCenter.Pages
{
    internal sealed class DatabaseGmPage : BufferedPanel
    {
        private readonly BackendService backend;
        private readonly TextBox txtLogin;
        private readonly TextBox txtPassword;
        private readonly TextBox txtCharName;
        private readonly Button btnGmLevel;
        private string selectedGmRole = "IMPLEMENTOR";
        private readonly TextBox txtCoins;
        private readonly TextBox txtClientVersion;
        private readonly DataGridView gridAccounts;
        private readonly DataGridView gridGms;

        public DatabaseGmPage(BackendService backend)
        {
            this.backend = backend;
            Dock = DockStyle.Fill;
            BackColor = Theme.BgMain;
            Padding = new Padding(8, 6, 8, 6);

            // Top Compact Form Card (Height = 104)
            var topCard = new BufferedPanel
            {
                Dock = DockStyle.Top,
                Height = 104,
                BackColor = Theme.BgCard,
                DrawCardBorder = true,
                Padding = new Padding(10, 6, 10, 6)
            };

            AddLbl(topCard, "Hesap ID:", 10, 10);
            txtLogin = Theme.CreateTextBox("admin");
            txtLogin.Location = new Point(72, 7);
            txtLogin.Size = new Size(100, 22);

            AddLbl(topCard, "Şifre:", 180, 10);
            txtPassword = Theme.CreateTextBox("12345");
            txtPassword.Location = new Point(216, 7);
            txtPassword.Size = new Size(90, 22);

            AddLbl(topCard, "Karakter:", 314, 10);
            txtCharName = Theme.CreateTextBox("");
            txtCharName.Location = new Point(372, 7);
            txtCharName.Size = new Size(100, 22);

            AddLbl(topCard, "Yetki:", 480, 10);
            btnGmLevel = Theme.CreateButton("IMPLEMENTOR ▾", ButtonStyle.Secondary, 125, 22);
            btnGmLevel.Location = new Point(518, 7);
            btnGmLevel.Font = Theme.FontButtonSm;
            var gmRoles = new[] { "IMPLEMENTOR", "HIGH_WIZARD", "GOD", "LOW_WIZARD", "YETKİ YOK" };
            btnGmLevel.Click += (s, e) =>
            {
                int idx = Array.IndexOf(gmRoles, selectedGmRole);
                selectedGmRole = gmRoles[(idx + 1) % gmRoles.Length];
                btnGmLevel.Text = selectedGmRole + " ▾";
            };

            AddLbl(topCard, "EP:", 650, 10);
            txtCoins = Theme.CreateTextBox("0");
            txtCoins.Location = new Point(676, 7);
            txtCoins.Size = new Size(112, 22);

            // Row 2: Action Buttons
            var btnSaveAcc = Theme.CreateButton("✓ HESAP & GM KAYDET", ButtonStyle.PrimaryCrimson, 195, 28);
            btnSaveAcc.Location = new Point(10, 36);
            btnSaveAcc.Click += (s, e) => SaveAccountAndGm();

            var btnDelGm = Theme.CreateButton("✕ GM SİL", ButtonStyle.Secondary, 90, 28);
            btnDelGm.Location = new Point(210, 36);
            btnDelGm.Click += (s, e) => RemoveGmRole();

            var btnBan = Theme.CreateButton("BAN / AÇ", ButtonStyle.Danger, 90, 28);
            btnBan.Location = new Point(305, 36);
            btnBan.Click += (s, e) => ToggleBanAccount();

            AddLbl(topCard, "Versiyon:", 405, 42);
            txtClientVersion = Theme.CreateTextBox("1000138963");
            txtClientVersion.Location = new Point(463, 39);
            txtClientVersion.Size = new Size(88, 22);

            var btnVer = Theme.CreateButton("KAYDET", ButtonStyle.PrimaryGold, 78, 28);
            btnVer.Location = new Point(555, 36);
            btnVer.Click += (s, e) => UpdateClientVersion();

            var btnBackup = Theme.CreateButton("💾 DB YEDEK", ButtonStyle.Success, 151, 28);
            btnBackup.Location = new Point(638, 36);
            btnBackup.Click += async (s, e) => await BackupDatabasesAsync();

            // Row 3: Quick Schema & Refresh
            var lblHint = new Label
            {
                Text = "Tablodan bir hesaba tıklayarak bilgileri yukarıya otomatik doldurabilirsiniz.",
                Font = Theme.FontSmall,
                ForeColor = Theme.TextMuted,
                Location = new Point(10, 73),
                AutoSize = true
            };

            var btnInitDb = Theme.CreateButton("⚡ ŞEMALARI ONAR", ButtonStyle.Secondary, 145, 25);
            btnInitDb.Location = new Point(525, 69);
            btnInitDb.Font = Theme.FontButtonSm;
            btnInitDb.Click += async (s, e) =>
            {
                await backend.RunPowerShellScriptAsync("Veritabanı Şema Kurulumu", "setup-database.ps1");
                RefreshTables();
            };

            var btnRefresh = Theme.CreateButton("↻ YENİLE", ButtonStyle.Secondary, 114, 25);
            btnRefresh.Location = new Point(675, 69);
            btnRefresh.Font = Theme.FontButtonSm;
            btnRefresh.Click += (s, e) => RefreshTables();

            topCard.Controls.AddRange(new Control[]
            {
                txtLogin, txtPassword, txtCharName, btnGmLevel, txtCoins,
                btnSaveAcc, btnDelGm, btnBan, txtClientVersion, btnVer, btnBackup,
                lblHint, btnInitDb, btnRefresh
            });

            // Bottom Split Grids
            var split = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 2,
                RowCount = 1,
                BackColor = Color.Transparent,
                Padding = new Padding(0, 6, 0, 0)
            };
            split.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 58F));
            split.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 42F));

            var leftCard = new BufferedPanel { Dock = DockStyle.Fill, BackColor = Theme.BgCard, DrawCardBorder = true, Margin = new Padding(0, 0, 4, 0), Padding = new Padding(6) };
            gridAccounts = Theme.CreateGrid();
            gridAccounts.Dock = DockStyle.Fill;
            gridAccounts.Columns.Add("Id", "ID");
            gridAccounts.Columns.Add("Login", "Hesap");
            gridAccounts.Columns.Add("Status", "Durum");
            gridAccounts.Columns.Add("Coins", "EP");
            gridAccounts.Columns.Add("Chars", "Karakterler");
            gridAccounts.Columns["Id"].FillWeight = 35;
            gridAccounts.Columns["Status"].FillWeight = 45;
            gridAccounts.Columns["Coins"].FillWeight = 45;
            gridAccounts.SelectionChanged += (s, e) =>
            {
                if (gridAccounts.SelectedRows.Count == 0) return;
                var r = gridAccounts.SelectedRows[0];
                txtLogin.Text = Convert.ToString(r.Cells["Login"].Value);
                txtCoins.Text = Convert.ToString(r.Cells["Coins"].Value);
                string chars = Convert.ToString(r.Cells["Chars"].Value);
                if (!string.IsNullOrWhiteSpace(chars) && chars != "-")
                    txtCharName.Text = chars.Split(',')[0].Trim();
            };
            leftCard.Controls.Add(gridAccounts);
            Theme.AttachGridScrollBar(gridAccounts, leftCard);

            var rightCard = new BufferedPanel { Dock = DockStyle.Fill, BackColor = Theme.BgCard, DrawCardBorder = true, Margin = new Padding(4, 0, 0, 0), Padding = new Padding(6) };
            gridGms = Theme.CreateGrid();
            gridGms.Dock = DockStyle.Fill;
            gridGms.Columns.Add("mID", "ID");
            gridGms.Columns.Add("mAccount", "Hesap");
            gridGms.Columns.Add("mName", "Karakter");
            gridGms.Columns.Add("mAuthority", "Yetki");
            gridGms.Columns["mID"].FillWeight = 35;
            gridGms.SelectionChanged += (s, e) =>
            {
                if (gridGms.SelectedRows.Count == 0) return;
                var r = gridGms.SelectedRows[0];
                txtLogin.Text = Convert.ToString(r.Cells["mAccount"].Value);
                txtCharName.Text = Convert.ToString(r.Cells["mName"].Value);
            };
            rightCard.Controls.Add(gridGms);
            Theme.AttachGridScrollBar(gridGms, rightCard);

            split.Controls.Add(leftCard, 0, 0);
            split.Controls.Add(rightCard, 1, 0);

            Controls.Add(split);
            Controls.Add(topCard);

            RefreshTables();
        }

        private static void AddLbl(Control p, string text, int x, int y)
        {
            p.Controls.Add(new Label { Text = text, Location = new Point(x, y), AutoSize = true, Font = Theme.FontSmall, ForeColor = Theme.TextMain });
        }

        private static string EscSql(string s) { return (s ?? "").Replace("\\", "\\\\").Replace("'", "\\'"); }

        private void SaveAccountAndGm()
        {
            string login = txtLogin.Text.Trim();
            string pass = txtPassword.Text;
            string charName = txtCharName.Text.Trim();
            string gmRole = selectedGmRole;
            int coins = 0;
            int.TryParse(txtCoins.Text.Trim(), out coins);
            if (string.IsNullOrEmpty(login)) return;

            string sql = !string.IsNullOrEmpty(pass)
                ? string.Format("INSERT INTO account.account (login, password, social_id, email, status, cash) VALUES ('{0}', PASSWORD('{1}'), '1234567', 'admin@local', 'OK', {2}) ON DUPLICATE KEY UPDATE password=PASSWORD('{1}'), status='OK', cash={2}; ", EscSql(login), EscSql(pass), coins)
                : string.Format("UPDATE account.account SET cash={0}, status='OK' WHERE login='{1}'; ", coins, EscSql(login));

            if (!string.IsNullOrEmpty(charName) && gmRole != "YETKİ YOK")
            {
                sql += string.Format("DELETE FROM common.gmlist WHERE mName='{1}'; INSERT INTO common.gmlist (mAccount, mName, mContactIP, mServerIP, mAuthority) VALUES ('{0}', '{1}', 'ALL', 'ALL', '{2}');", EscSql(login), EscSql(charName), EscSql(gmRole));
            }
            string err;
            backend.RunSqlQuery(sql, null, out err);
            if (!string.IsNullOrEmpty(err)) backend.EmitLog("[SQL HATA] " + err, true);
            else { backend.EmitLog("Hesap/GM kaydedildi: " + login, false); RefreshTables(); }
        }

        private void RemoveGmRole()
        {
            string charName = txtCharName.Text.Trim();
            string login = txtLogin.Text.Trim();
            string where = !string.IsNullOrEmpty(charName) ? ("mName='" + EscSql(charName) + "'") : ("mAccount='" + EscSql(login) + "'");
            string err;
            backend.RunSqlQuery("DELETE FROM common.gmlist WHERE " + where + ";", null, out err);
            RefreshTables();
        }

        private void ToggleBanAccount()
        {
            string login = txtLogin.Text.Trim();
            if (string.IsNullOrEmpty(login)) return;
            string err;
            backend.RunSqlQuery("UPDATE account.account SET status = IF(status='OK','BLOCK','OK') WHERE login='" + EscSql(login) + "';", null, out err);
            RefreshTables();
        }

        private void UpdateClientVersion()
        {
            string ver = txtClientVersion.Text.Trim();
            if (string.IsNullOrEmpty(ver)) return;
            string err;
            backend.RunSqlQuery("UPDATE common.game_settings SET version=" + EscSql(ver) + ";", null, out err);
            backend.EmitLog("Client versiyonu güncellendi: " + ver, false);
        }

        private async Task BackupDatabasesAsync()
        {
            string backupDir = Path.Combine(backend.ProjectRoot, @"database\backups");
            Directory.CreateDirectory(backupDir);
            string outFile = Path.Combine(backupDir, "valiant2_" + DateTime.Now.ToString("yyyyMMdd_HHmmss") + ".sql");
            string script = string.Format(@"
. '{0}'
$settings = Get-EnvSettings
$mariaBin = Join-Path (Get-MariaDbDir) 'bin'
$dumpExe = Join-Path $mariaBin 'mariadb-dump.exe'
$env:MYSQL_PWD = $settings['MARIADB_ROOT_PASSWORD']
& cmd.exe /c ""`""$dumpExe`"" --host=$($settings.MYSQL_HOST) --port=$($settings.MYSQL_PORT) --user=root --databases account common log player > `""{1}`""""
Write-Host 'Yedek alindi: {1}'
", Path.Combine(backend.ScriptsDir, "common.ps1"), outFile);
            await backend.RunPowerShellInlineAsync("Veritabanı Yedeği Alınıyor", script);
        }

        public void RefreshTables()
        {
            Task.Run(() =>
            {
                if (!BackendService.CheckTcpPort(3306)) return;
                string e1, e2, e3;
                string accOut = backend.RunSqlQuery("SELECT a.id, a.login, a.status, IFNULL(a.cash, 0), IFNULL(GROUP_CONCAT(p.name SEPARATOR ', '), '-') FROM account.account a LEFT JOIN player.player p ON p.account_id = a.id GROUP BY a.id ORDER BY a.id DESC LIMIT 100;", null, out e1);
                string gmOut = backend.RunSqlQuery("SELECT mID, mAccount, mName, mAuthority FROM common.gmlist ORDER BY mID DESC;", null, out e2);
                string verOut = backend.RunSqlQuery("SELECT version FROM common.game_settings LIMIT 1;", null, out e3);

                if (IsDisposed) return;
                BeginInvoke(new Action(() =>
                {
                    if (string.IsNullOrEmpty(e1) && !string.IsNullOrWhiteSpace(accOut))
                    {
                        gridAccounts.Rows.Clear();
                        var lines = accOut.Split(new[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);
                        for (int i = 1; i < lines.Length; i++)
                        {
                            var cols = lines[i].Split('\t');
                            if (cols.Length >= 5) gridAccounts.Rows.Add(cols[0], cols[1], cols[2], cols[3], cols[4]);
                        }
                    }
                    if (string.IsNullOrEmpty(e2) && !string.IsNullOrWhiteSpace(gmOut))
                    {
                        gridGms.Rows.Clear();
                        var lines = gmOut.Split(new[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);
                        for (int i = 1; i < lines.Length; i++)
                        {
                            var cols = lines[i].Split('\t');
                            if (cols.Length >= 4) gridGms.Rows.Add(cols[0], cols[1], cols[2], cols[3]);
                        }
                    }
                    if (string.IsNullOrEmpty(e3) && !string.IsNullOrWhiteSpace(verOut))
                    {
                        var lines = verOut.Split(new[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);
                        if (lines.Length >= 2) txtClientVersion.Text = lines[1].Trim();
                    }
                }));
            });
        }
    }
}
