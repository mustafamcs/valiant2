using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Security.Principal;
using System.ServiceProcess;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;

namespace Valiant2ControlCenter
{
    internal sealed class ServiceHealthSnapshot
    {
        public bool MariaDbRunning;
        public bool DbPeerOpen;
        public bool AuthOpen;
        public bool Ch1Core1Open;
        public bool Ch1Core2Open;
        public bool Ch1Core3Open;
        public bool Ch1Core4Open;
        public bool Ch99Open;
        public bool NginxRunning;
        public int NginxProcessCount;
        public int PhpWorkerCount;
        public bool PatchFileServerOpen;
        public bool PatchWatcherRunning;

        public string PublicIp = "127.0.0.1";
        public string ServerName = "VALIANT2";
        public string ClientVersion = "-";
        public int PatchVersion = 0;
        public int PatchFileCount = 0;
        public int AccountCount = 0;
        public int CharacterCount = 0;
        public int GmCount = 0;

        public int RunningGameCoresCount
        {
            get
            {
                int c = 0;
                if (DbPeerOpen) c++;
                if (AuthOpen) c++;
                if (Ch1Core1Open) c++;
                if (Ch1Core2Open) c++;
                if (Ch1Core3Open) c++;
                if (Ch1Core4Open) c++;
                if (Ch99Open) c++;
                return c;
            }
        }

        public bool WebStackHealthy
        {
            get { return NginxRunning && PhpWorkerCount >= 1 && PatchFileServerOpen && PatchWatcherRunning; }
        }
    }

    internal sealed class PackEntryInfo
    {
        public string Name;
        public string SourceDir;
        public string PakFile;
        public bool Exists;
        public long SizeBytes;
        public DateTime LastModified;
    }

    internal sealed class ProcessEntryInfo
    {
        public string Role;
        public string ProcessName;
        public int Pid;
        public double MemoryMb;
        public string WorkingDir;
        public string Status;
    }

    internal sealed class SetupStepState
    {
        public string Id;
        public string Title;
        public string Description;
        public bool IsReady;
        public string StatusDetail;
    }

    internal sealed class BackendService
    {
        public string ProjectRoot { get; private set; }
        public string ScriptsDir { get { return Path.Combine(ProjectRoot, @"scripts\windows"); } }
        public string EnvFilePath { get { return Path.Combine(ProjectRoot, ".env"); } }

        public string CpuName { get; private set; }
        public int CpuCores { get; private set; }
        public int CpuThreads { get; private set; }
        public double TotalRamGb { get; private set; }
        public string HardwareSummary { get; private set; }

        private Process activeProcess;
        private readonly object procLock = new object();

        public event Action<string, bool> OnOutputLine;
        public event Action<string, bool> OnTaskStateChanged;

        public bool IsBusy
        {
            get { lock (procLock) { return activeProcess != null && !activeProcess.HasExited; } }
        }

        public BackendService()
        {
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12 | (SecurityProtocolType)0x3000;
            ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
            ProjectRoot = ResolveProjectRoot();
            DetectHardwareProfile();
            EnsureMachineEnvValidOnStartup();
        }

        public static List<string> GetLocalAdapterIps()
        {
            var list = new List<string>();
            try
            {
                foreach (var ni in System.Net.NetworkInformation.NetworkInterface.GetAllNetworkInterfaces())
                {
                    if (ni.OperationalStatus != System.Net.NetworkInformation.OperationalStatus.Up) continue;
                    if (ni.NetworkInterfaceType == System.Net.NetworkInformation.NetworkInterfaceType.Loopback) continue;
                    var props = ni.GetIPProperties();
                    foreach (var ua in props.UnicastAddresses)
                    {
                        if (ua.Address.AddressFamily == AddressFamily.InterNetwork)
                        {
                            string ip = ua.Address.ToString();
                            if (!ip.StartsWith("127.") && !ip.StartsWith("169.254."))
                                list.Add(ip);
                        }
                    }
                }
            }
            catch { }
            return list;
        }

        public static HashSet<int> GetActiveListeningPorts()
        {
            var set = new HashSet<int>();
            try
            {
                var endpoints = System.Net.NetworkInformation.IPGlobalProperties.GetIPGlobalProperties().GetActiveTcpListeners();
                for (int i = 0; i < endpoints.Length; i++)
                {
                    set.Add(endpoints[i].Port);
                }
            }
            catch { }
            return set;
        }

        public static string FetchExternalWanIp()
        {
            string[] urls = { "https://api.ipify.org", "https://ifconfig.me/ip", "https://icanhazip.com" };
            foreach (var url in urls)
            {
                try
                {
                    var req = (HttpWebRequest)WebRequest.Create(url);
                    req.Timeout = 2500;
                    req.UserAgent = "curl/8.0";
                    using (var resp = req.GetResponse())
                    using (var sr = new StreamReader(resp.GetResponseStream()))
                    {
                        string ip = sr.ReadToEnd().Trim();
                        if (Regex.IsMatch(ip, @"^\d{1,3}(\.\d{1,3}){3}$"))
                            return ip;
                    }
                }
                catch { }
            }
            return null;
        }

        public static bool IsIpReachableOnThisMachine(string testIp)
        {
            if (string.IsNullOrWhiteSpace(testIp)) return false;
            if (testIp == "127.0.0.1") return true;
            var localIps = GetLocalAdapterIps();
            if (localIps.Contains(testIp)) return true;

            string extIp = FetchExternalWanIp();
            if (string.IsNullOrEmpty(extIp) || !string.Equals(testIp, extIp, StringComparison.OrdinalIgnoreCase))
                return false;

            var listening = GetActiveListeningPorts();
            int[] checkPorts = { 443, 80, 30001 };
            foreach (int p in checkPorts)
            {
                if (listening.Contains(p))
                {
                    try
                    {
                        using (var client = new TcpClient())
                        {
                            var ar = client.BeginConnect(testIp, p, null, null);
                            if (ar.AsyncWaitHandle.WaitOne(1200) && client.Connected) return true;
                        }
                    }
                    catch { }
                }
            }

            TcpListener listener = null;
            try
            {
                listener = new TcpListener(IPAddress.Any, 30001);
                listener.Start();
                using (var client = new TcpClient())
                {
                    var ar = client.BeginConnect(testIp, 30001, null, null);
                    bool ok = ar.AsyncWaitHandle.WaitOne(1200);
                    if (ok)
                    {
                        for (int w = 0; w < 10; w++)
                        {
                            if (client.Connected || listener.Pending()) return true;
                            Thread.Sleep(20);
                        }
                    }
                    return false;
                }
            }
            catch { return false; }
            finally
            {
                if (listener != null) { try { listener.Stop(); } catch { } }
            }
        }

        public string DetectPublicIp()
        {
            var localIps = GetLocalAdapterIps();
            string extIp = FetchExternalWanIp();
            if (!string.IsNullOrEmpty(extIp))
            {
                if (localIps.Contains(extIp) || IsIpReachableOnThisMachine(extIp))
                    return extIp;
            }
            if (localIps.Count > 0)
                return localIps[0];
            return "127.0.0.1";
        }

        public static bool StripUtf8BomIfPresent(string path)
        {
            try
            {
                if (!File.Exists(path)) return false;
                byte[] bytes = File.ReadAllBytes(path);
                if (bytes.Length >= 3 && bytes[0] == 0xEF && bytes[1] == 0xBB && bytes[2] == 0xBF)
                {
                    byte[] clean = new byte[bytes.Length - 3];
                    Buffer.BlockCopy(bytes, 3, clean, 0, clean.Length);
                    File.WriteAllBytes(path, clean);
                    return true;
                }
            }
            catch { }
            return false;
        }

        public void RepairAllBomFiles()
        {
            string[] fixedTargets =
            {
                EnvFilePath,
                Path.Combine(ProjectRoot, @"runtime\dependencies\nginx\conf\nginx.conf"),
                Path.Combine(ProjectRoot, @"runtime\dependencies\mariadb\data\my.ini"),
                Path.Combine(ProjectRoot, @"runtime\patchserver\patchserver.json"),
                Path.Combine(ProjectRoot, @"runtime\patchserver\patch\patchlist.json"),
                Path.Combine(ProjectRoot, @"runtime\patchserver\patch\patcher.json"),
                Path.Combine(ProjectRoot, @"runtime\patchserver\patch\hashcache.json"),
                Path.Combine(ProjectRoot, @"assets\unpacked\data\root\serverinfo.py"),
                Path.Combine(ProjectRoot, @"source\client\external\projects\CRootLib\Workplace\__cython\root_modules\serverinfo.py")
            };
            foreach (var t in fixedTargets) StripUtf8BomIfPresent(t);

            string srvRoot = Path.Combine(ProjectRoot, @"runtime\server\main\srv1");
            if (Directory.Exists(srvRoot))
            {
                string[] coreRelDirs =
                {
                    "auth", "db", @"share\conf",
                    @"chan\ch1\core1", @"chan\ch1\core2", @"chan\ch1\core3", @"chan\ch1\core4",
                    @"chan\ch99\core99"
                };
                string[] names = { "CONFIG", "conf.txt", "CMD", "CRC", "VERSION", "BANIP" };
                foreach (var rel in coreRelDirs)
                {
                    string d = Path.Combine(srvRoot, rel);
                    if (!Directory.Exists(d)) continue;
                    foreach (var n in names)
                    {
                        StripUtf8BomIfPresent(Path.Combine(d, n));
                    }
                }
            }
            try
            {
                if (Directory.Exists(ScriptsDir))
                {
                    foreach (var f in Directory.GetFiles(ScriptsDir))
                    {
                        if (f.EndsWith(".ps1", StringComparison.OrdinalIgnoreCase) ||
                            f.EndsWith(".cmd", StringComparison.OrdinalIgnoreCase) ||
                            f.EndsWith(".py", StringComparison.OrdinalIgnoreCase))
                        {
                            StripUtf8BomIfPresent(f);
                        }
                    }
                }
                string unpackedDir = Path.Combine(ProjectRoot, @"assets\unpacked");
                if (Directory.Exists(unpackedDir))
                {
                    foreach (var f in Directory.GetFiles(unpackedDir, "*.bat"))
                        StripUtf8BomIfPresent(f);
                }
            }
            catch { }
        }

        private void EnsureMachineEnvValidOnStartup()
        {
            try
            {
                RepairAllBomFiles();
                string expectedPatchRoot = Path.Combine(ProjectRoot, @"runtime\patchserver");
                if (!File.Exists(EnvFilePath))
                {
                    SaveEnv(GenerateDefaultEnv());
                    return;
                }
                var env = LoadEnv();
                bool changed = false;
                var expectedPaths = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
                {
                    { "PROJECT_ROOT", ProjectRoot },
                    { "PATCH_ROOT", expectedPatchRoot },
                    { "NGINX_DIR", Path.Combine(ProjectRoot, @"runtime\dependencies\nginx") },
                    { "MARIADB_DIR", Path.Combine(ProjectRoot, @"runtime\dependencies\mariadb") }
                };
                foreach (var kv in expectedPaths)
                {
                    if (!env.ContainsKey(kv.Key) || !string.Equals(env[kv.Key], kv.Value, StringComparison.OrdinalIgnoreCase))
                    {
                        env[kv.Key] = kv.Value;
                        changed = true;
                    }
                }
                string curIp = env.ContainsKey("PUBLIC_IP") ? env["PUBLIC_IP"] : "";
                if (!IsIpReachableOnThisMachine(curIp))
                {
                    string smartIp = DetectPublicIp();
                    env["PUBLIC_IP"] = smartIp;
                    env["CLIENT_SERVER_IP"] = smartIp;
                    env["PANEL_BASE_URL"] = "https://" + smartIp + "/";
                    changed = true;
                }
                if (changed)
                {
                    SaveEnv(env);
                }
            }
            catch { }
        }

        private void DetectHardwareProfile()
        {
            CpuThreads = Math.Max(1, Environment.ProcessorCount);
            CpuCores = Math.Max(1, CpuThreads / 2);
            CpuName = "Multi-Core CPU";
            TotalRamGb = 16.0;
            try
            {
                using (var reg = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(@"HARDWARE\DESCRIPTION\System\CentralProcessor\0"))
                {
                    if (reg != null)
                    {
                        var nameObj = reg.GetValue("ProcessorNameString");
                        if (nameObj != null) CpuName = nameObj.ToString().Trim();
                    }
                }
                var memStatus = new MEMORYSTATUSEX();
                if (GlobalMemoryStatusEx(memStatus))
                {
                    TotalRamGb = Math.Round(memStatus.ullTotalPhys / (1024.0 * 1024.0 * 1024.0), 1);
                }
            }
            catch { }
            HardwareSummary = string.Format("{0} ({1}C/{2}T • {3:0.0} GB RAM)", CpuName, CpuCores, CpuThreads, TotalRamGb);
        }

        [System.Runtime.InteropServices.StructLayout(System.Runtime.InteropServices.LayoutKind.Sequential, CharSet = System.Runtime.InteropServices.CharSet.Auto)]
        private class MEMORYSTATUSEX
        {
            public uint dwLength = (uint)System.Runtime.InteropServices.Marshal.SizeOf(typeof(MEMORYSTATUSEX));
            public uint dwMemoryLoad;
            public ulong ullTotalPhys;
            public ulong ullAvailPhys;
            public ulong ullTotalPageFile;
            public ulong ullAvailPageFile;
            public ulong ullTotalVirtual;
            public ulong ullAvailVirtual;
            public ulong ullAvailExtendedVirtual;
        }

        [System.Runtime.InteropServices.DllImport("kernel32.dll", CharSet = System.Runtime.InteropServices.CharSet.Auto, SetLastError = true)]
        private static extern bool GlobalMemoryStatusEx([System.Runtime.InteropServices.In, System.Runtime.InteropServices.Out] MEMORYSTATUSEX lpBuffer);

        private static string ResolveProjectRoot()
        {
            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            DirectoryInfo dir = new DirectoryInfo(baseDir);
            while (dir != null)
            {
                if (Directory.Exists(Path.Combine(dir.FullName, @"scripts\windows")) &&
                    File.Exists(Path.Combine(dir.FullName, @"scripts\windows\common.ps1")))
                {
                    return dir.FullName;
                }
                dir = dir.Parent;
            }
            string cwd = Directory.GetCurrentDirectory();
            if (Directory.Exists(Path.Combine(cwd, @"scripts\windows")))
                return cwd;
            return baseDir.TrimEnd('\\', '/');
        }

        public static bool IsAdministrator()
        {
            try
            {
                var identity = WindowsIdentity.GetCurrent();
                var principal = new WindowsPrincipal(identity);
                return principal.IsInRole(WindowsBuiltInRole.Administrator);
            }
            catch { return false; }
        }

        public Dictionary<string, string> LoadEnv()
        {
            var dict = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
            if (!File.Exists(EnvFilePath)) return dict;
            StripUtf8BomIfPresent(EnvFilePath);
            foreach (var raw in File.ReadAllLines(EnvFilePath, Encoding.UTF8))
            {
                var line = raw.Trim().TrimStart('\uFEFF', '\u200B');
                if (string.IsNullOrEmpty(line) || line.StartsWith("#") || !line.Contains("=")) continue;
                int idx = line.IndexOf('=');
                string k = line.Substring(0, idx).Trim().TrimStart('\uFEFF', '\u200B');
                string v = line.Substring(idx + 1).Trim().Trim('"', '\'');
                dict[k] = v;
            }
            return dict;
        }

        public void SaveEnv(Dictionary<string, string> settings)
        {
            var orderedKeys = new[]
            {
                "PROJECT_ROOT",
                "MYSQL_HOST", "MYSQL_PORT", "MYSQL_USER", "MYSQL_PASSWORD",
                "MYSQL_ACCOUNT_DATABASE", "MYSQL_COMMON_DATABASE", "MYSQL_LOG_DATABASE", "MYSQL_PLAYER_DATABASE",
                "SERVER_DB_HOST", "SERVER_DB_PORT",
                "ADMINPAGE_IP", "ADMINPAGE_PASSWORD",
                "CLIENT_SERVER_NAME", "CLIENT_SERVER_IP",
                "MARIADB_SERVICE", "MARIADB_ROOT_PASSWORD",
                "PANEL_DB_DATABASE", "PANEL_DB_USER", "PANEL_DB_PASSWORD",
                "PANEL_P2P_CHANNEL_PORTS", "PUBLIC_IP", "PANEL_BASE_URL", "PATCH_ROOT",
                "NGINX_DIR", "MARIADB_DIR"
            };

            var sb = new StringBuilder();
            var written = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            foreach (var k in orderedKeys)
            {
                if (settings.ContainsKey(k))
                {
                    sb.AppendLine(k + "=" + settings[k]);
                    written.Add(k);
                }
            }
            foreach (var kv in settings)
            {
                if (!written.Contains(kv.Key))
                    sb.AppendLine(kv.Key + "=" + kv.Value);
            }
            File.WriteAllText(EnvFilePath, sb.ToString(), new UTF8Encoding(false));
        }

        public Dictionary<string, string> GenerateDefaultEnv(string detectedIp = null)
        {
            if (string.IsNullOrWhiteSpace(detectedIp))
                detectedIp = DetectPublicIp();

            Func<string> newPass = () => Guid.NewGuid().ToString("N");
            var existing = LoadEnv();
            Func<string, string, string> getOr = (k, def) =>
                existing.ContainsKey(k) && !string.IsNullOrWhiteSpace(existing[k]) ? existing[k] : def;

            var d = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
            {
                { "MYSQL_HOST", getOr("MYSQL_HOST", "127.0.0.1") },
                { "MYSQL_PORT", getOr("MYSQL_PORT", "3306") },
                { "MYSQL_USER", getOr("MYSQL_USER", "valiant2") },
                { "MYSQL_PASSWORD", getOr("MYSQL_PASSWORD", newPass()) },
                { "MYSQL_ACCOUNT_DATABASE", getOr("MYSQL_ACCOUNT_DATABASE", "account") },
                { "MYSQL_COMMON_DATABASE", getOr("MYSQL_COMMON_DATABASE", "common") },
                { "MYSQL_LOG_DATABASE", getOr("MYSQL_LOG_DATABASE", "log") },
                { "MYSQL_PLAYER_DATABASE", getOr("MYSQL_PLAYER_DATABASE", "player") },
                { "SERVER_DB_HOST", getOr("SERVER_DB_HOST", "127.0.0.1") },
                { "SERVER_DB_PORT", getOr("SERVER_DB_PORT", "30000") },
                { "ADMINPAGE_IP", getOr("ADMINPAGE_IP", "127.0.0.1") },
                { "ADMINPAGE_PASSWORD", getOr("ADMINPAGE_PASSWORD", newPass()) },
                { "CLIENT_SERVER_NAME", getOr("CLIENT_SERVER_NAME", "VALIANT2") },
                { "CLIENT_SERVER_IP", detectedIp },
                { "MARIADB_SERVICE", getOr("MARIADB_SERVICE", "MariaDB") },
                { "MARIADB_ROOT_PASSWORD", getOr("MARIADB_ROOT_PASSWORD", newPass()) },
                { "PANEL_DB_DATABASE", getOr("PANEL_DB_DATABASE", "valiant_panel") },
                { "PANEL_DB_USER", getOr("PANEL_DB_USER", "valiant_panel") },
                { "PANEL_DB_PASSWORD", getOr("PANEL_DB_PASSWORD", newPass()) },
                { "PANEL_P2P_CHANNEL_PORTS", getOr("PANEL_P2P_CHANNEL_PORTS", "30003,30005,30007,30009,30051") },
                { "PUBLIC_IP", detectedIp },
                { "PANEL_BASE_URL", "https://" + detectedIp + "/" },
                { "PROJECT_ROOT", ProjectRoot },
                { "PATCH_ROOT", Path.Combine(ProjectRoot, @"runtime\patchserver") },
                { "NGINX_DIR", Path.Combine(ProjectRoot, @"runtime\dependencies\nginx") },
                { "MARIADB_DIR", Path.Combine(ProjectRoot, @"runtime\dependencies\mariadb") }
            };
            return d;
        }

        public static bool CheckTcpPort(int port, int timeoutMs = 250)
        {
            return GetActiveListeningPorts().Contains(port);
        }

        public string FindMysqlExe(string exeName = "mariadb.exe")
        {
            string projBin = Path.Combine(ProjectRoot, @"runtime\dependencies\mariadb\bin");
            if (Directory.Exists(projBin))
            {
                string p1 = Path.Combine(projBin, exeName);
                if (File.Exists(p1)) return p1;
                string p2 = Path.Combine(projBin, exeName == "mariadb-dump.exe" ? "mysqldump.exe" : "mysql.exe");
                if (File.Exists(p2)) return p2;
            }
            string progFiles = Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles);
            if (Directory.Exists(progFiles))
            {
                try
                {
                    foreach (var d in Directory.GetDirectories(progFiles, "MariaDB*"))
                    {
                        string p = Path.Combine(d, "bin", exeName);
                        if (File.Exists(p)) return p;
                    }
                }
                catch { }
            }
            return null;
        }

        public string RunSqlQuery(string sql, string database, out string error)
        {
            error = null;
            string mysqlExe = FindMysqlExe("mariadb.exe");
            if (string.IsNullOrEmpty(mysqlExe))
            {
                error = "MariaDB istemcisi (mariadb.exe) bulunamadı.";
                return "";
            }
            var env = LoadEnv();
            string host = env.ContainsKey("MYSQL_HOST") ? env["MYSQL_HOST"] : "127.0.0.1";
            string port = env.ContainsKey("MYSQL_PORT") ? env["MYSQL_PORT"] : "3306";
            string rootPass = env.ContainsKey("MARIADB_ROOT_PASSWORD") ? env["MARIADB_ROOT_PASSWORD"] : "";

            var args = new StringBuilder();
            args.AppendFormat("--host={0} --port={1} --user=root --batch --raw --default-character-set=utf8mb4 ", host, port);
            if (!string.IsNullOrEmpty(database))
                args.AppendFormat("\"{0}\" ", database);
            args.AppendFormat("-e \"{0}\"", sql.Replace("\"", "\\\""));

            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = mysqlExe,
                    Arguments = args.ToString(),
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true,
                    StandardOutputEncoding = Encoding.UTF8,
                    StandardErrorEncoding = Encoding.UTF8
                };
                psi.EnvironmentVariables["MYSQL_PWD"] = rootPass;
                using (var proc = Process.Start(psi))
                {
                    string stdout = proc.StandardOutput.ReadToEnd();
                    string stderr = proc.StandardError.ReadToEnd();
                    proc.WaitForExit(8000);
                    if (proc.ExitCode != 0)
                    {
                        error = string.IsNullOrWhiteSpace(stderr) ? ("SQL çıkış kodu: " + proc.ExitCode) : stderr.Trim();
                    }
                    return stdout;
                }
            }
            catch (Exception ex)
            {
                error = ex.Message;
                return "";
            }
        }

        public ServiceHealthSnapshot GetHealthSnapshot()
        {
            var snap = new ServiceHealthSnapshot();
            var env = LoadEnv();
            if (env.ContainsKey("PUBLIC_IP") && !string.IsNullOrWhiteSpace(env["PUBLIC_IP"]))
                snap.PublicIp = env["PUBLIC_IP"];
            else if (env.ContainsKey("CLIENT_SERVER_IP") && !string.IsNullOrWhiteSpace(env["CLIENT_SERVER_IP"]))
                snap.PublicIp = env["CLIENT_SERVER_IP"];

            if (env.ContainsKey("CLIENT_SERVER_NAME") && !string.IsNullOrWhiteSpace(env["CLIENT_SERVER_NAME"]))
                snap.ServerName = env["CLIENT_SERVER_NAME"];

            var listening = GetActiveListeningPorts();
            snap.MariaDbRunning      = listening.Contains(3306);
            snap.DbPeerOpen          = listening.Contains(30000);
            snap.AuthOpen            = listening.Contains(30001);
            snap.Ch1Core1Open        = listening.Contains(30003);
            snap.Ch1Core2Open        = listening.Contains(30005);
            snap.Ch1Core3Open        = listening.Contains(30007);
            snap.Ch1Core4Open        = listening.Contains(30009);
            snap.Ch99Open            = listening.Contains(30051);
            snap.PatchFileServerOpen = listening.Contains(8091);

            int phpCount = 0;
            foreach (int p in new[] { 8090, 8092, 8093, 8094 })
            {
                if (listening.Contains(p)) phpCount++;
            }
            snap.PhpWorkerCount = phpCount;

            try
            {
                var nginxProcs = Process.GetProcessesByName("nginx");
                snap.NginxProcessCount = nginxProcs.Length;
                snap.NginxRunning = nginxProcs.Length > 0 || CheckTcpPort(443, 150) || CheckTcpPort(80, 150);
            }
            catch { }

            try
            {
                var pyProcs = Process.GetProcessesByName("pythonw");
                snap.PatchWatcherRunning = pyProcs.Length > 0;
            }
            catch { }

            // Patch manifest info
            try
            {
                string patchRoot = env.ContainsKey("PATCH_ROOT") && !string.IsNullOrWhiteSpace(env["PATCH_ROOT"])
                    ? env["PATCH_ROOT"]
                    : Path.Combine(ProjectRoot, @"runtime\patchserver");
                string patchList = Path.Combine(patchRoot, @"patch\patchlist.json");
                if (File.Exists(patchList))
                {
                    string json = File.ReadAllText(patchList);
                    var verMatch = Regex.Match(json, @"""version""\s*:\s*(\d+)");
                    if (verMatch.Success) int.TryParse(verMatch.Groups[1].Value, out snap.PatchVersion);
                    snap.PatchFileCount = Regex.Matches(json, @"""sha256""").Count;
                }
            }
            catch { }

            // DB Quick Counts if MariaDB is running
            if (snap.MariaDbRunning)
            {
                string err;
                string q = "SELECT " +
                           "(SELECT version FROM common.game_settings LIMIT 1) AS ver, " +
                           "(SELECT COUNT(*) FROM account.account) AS accs, " +
                           "(SELECT COUNT(*) FROM player.player) AS chars, " +
                           "(SELECT COUNT(*) FROM common.gmlist) AS gms;";
                string res = RunSqlQuery(q, null, out err);
                if (string.IsNullOrEmpty(err) && !string.IsNullOrWhiteSpace(res))
                {
                    var lines = res.Split(new[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);
                    if (lines.Length >= 2)
                    {
                        var cols = lines[1].Split('\t');
                        if (cols.Length >= 4)
                        {
                            snap.ClientVersion = cols[0];
                            int.TryParse(cols[1], out snap.AccountCount);
                            int.TryParse(cols[2], out snap.CharacterCount);
                            int.TryParse(cols[3], out snap.GmCount);
                        }
                    }
                }
            }

            return snap;
        }

        public List<ProcessEntryInfo> GetManagedProcesses()
        {
            var list = new List<ProcessEntryInfo>();
            string stateDir = Path.Combine(ProjectRoot, @"runtime\server\.state");
            var seenPids = new HashSet<int>();

            if (Directory.Exists(stateDir))
            {
                foreach (var pidFile in Directory.GetFiles(stateDir, "*.pid").OrderBy(x => x))
                {
                    string name = Path.GetFileNameWithoutExtension(pidFile);
                    int pid = 0;
                    int.TryParse(File.ReadAllText(pidFile).Trim(), out pid);
                    Process proc = null;
                    if (pid > 0)
                    {
                        try { proc = Process.GetProcessById(pid); } catch { }
                    }
                    if (proc != null && !proc.HasExited &&
                        (proc.ProcessName.Equals("db", StringComparison.OrdinalIgnoreCase) ||
                         proc.ProcessName.Equals("game", StringComparison.OrdinalIgnoreCase)))
                    {
                        seenPids.Add(pid);
                        list.Add(new ProcessEntryInfo
                        {
                            Role = name,
                            ProcessName = proc.ProcessName + ".exe",
                            Pid = pid,
                            MemoryMb = Math.Round(proc.WorkingSet64 / 1048576.0, 1),
                            WorkingDir = "runtime\\server\\main\\srv1",
                            Status = "Çalışıyor"
                        });
                    }
                    else
                    {
                        list.Add(new ProcessEntryInfo
                        {
                            Role = name,
                            ProcessName = "-",
                            Pid = pid,
                            MemoryMb = 0,
                            WorkingDir = "-",
                            Status = "Kapalı"
                        });
                    }
                }
            }

            string[] extraNames = { "db", "game", "nginx", "php", "pythonw", "M2Client" };
            foreach (var pName in extraNames)
            {
                try
                {
                    foreach (var p in Process.GetProcessesByName(pName))
                    {
                        if (seenPids.Contains(p.Id)) continue;
                        seenPids.Add(p.Id);
                        list.Add(new ProcessEntryInfo
                        {
                            Role = pName == "php" ? "panel-php-worker" : (pName == "pythonw" ? "patch-service" : pName),
                            ProcessName = p.ProcessName + ".exe",
                            Pid = p.Id,
                            MemoryMb = Math.Round(p.WorkingSet64 / 1048576.0, 1),
                            WorkingDir = "Arka Plan Servisi",
                            Status = "Çalışıyor"
                        });
                    }
                }
                catch { }
            }

            return list;
        }

        public List<SetupStepState> InspectSetupSteps()
        {
            var steps = new List<SetupStepState>();

            // 1. BuildTools & Compilers
            string vswhere = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), @"Microsoft Visual Studio\Installer\vswhere.exe");
            bool hasVs = File.Exists(vswhere);
            bool hasPy27 = File.Exists(@"C:\Python27\python.exe");
            steps.Add(new SetupStepState
            {
                Id = "deps",
                Title = "1. Derleme & Sistem Bağımlılıkları (Winget)",
                Description = "Git, Git LFS, VC++ Redist, .NET 4, VS2022 BuildTools, PHP 8.3 (curl/mysqli/pdo/gd), Python 3.12 ve Python 2.7",
                IsReady = hasVs && hasPy27,
                StatusDetail = (hasVs ? "VS2022 Hazır" : "VS2022 Eksik") + " | " + (hasPy27 ? "Python 2.7 Hazır" : "Python 2.7 Eksik")
            });

            // 2. .env
            bool hasEnv = File.Exists(EnvFilePath);
            var env = LoadEnv();
            steps.Add(new SetupStepState
            {
                Id = "env",
                Title = "2. Ortam Yapılandırması (.env) & Public IP",
                Description = "Dış IP otomatik algılanır, MySQL / AdminPage / Panel şifreleri güvenli olarak üretilir",
                IsReady = hasEnv && env.ContainsKey("PUBLIC_IP"),
                StatusDetail = hasEnv ? ("Hazır (IP: " + (env.ContainsKey("PUBLIC_IP") ? env["PUBLIC_IP"] : "-") + ")") : ".env Dosyası Yok"
            });

            // 3. MariaDB
            string mariaExe = Path.Combine(ProjectRoot, @"runtime\dependencies\mariadb\bin\mariadbd.exe");
            bool mariaInstalled = File.Exists(mariaExe);
            bool mariaPort = CheckTcpPort(3306, 150);
            steps.Add(new SetupStepState
            {
                Id = "mariadb",
                Title = "3. MariaDB 11.4 Portable & Windows Servisi",
                Description = "Proje içi taşınabilir MariaDB 11.4 indirilir, data dizini ve MariaDB servisi kurulur",
                IsReady = mariaInstalled && mariaPort,
                StatusDetail = mariaPort ? "Servis Çalışıyor (Port 3306)" : (mariaInstalled ? "İndirildi (Servis Kapalı)" : "Kurulu Değil")
            });

            // 4. Git LFS
            string samplePak = Path.Combine(ProjectRoot, @"assets\unpacked\FSArchiver.exe");
            bool lfsReady = File.Exists(samplePak) && new FileInfo(samplePak).Length > 10000;
            steps.Add(new SetupStepState
            {
                Id = "lfs",
                Title = "4. Git LFS Büyük Dosya Varlıkları",
                Description = "FSArchiver, kütüphaneler ve ikili varlık dosyaları Git LFS üzerinden indirilir",
                IsReady = lfsReady,
                StatusDetail = lfsReady ? "LFS Dosyaları Mevcut" : "LFS Pull Gerekli"
            });

            // 5. Nginx + SSL
            string nginxExe = Path.Combine(ProjectRoot, @"runtime\dependencies\nginx\nginx.exe");
            string certPem = Path.Combine(ProjectRoot, @"runtime\dependencies\nginx\certs\cert.pem");
            steps.Add(new SetupStepState
            {
                Id = "nginx",
                Title = "5. Nginx Web Sunucusu & SSL Sertifikası",
                Description = "Nginx 1.27.5 indirilir, Let's Encrypt IP / Self-Signed SSL sertifikası ve nginx.conf üretilir",
                IsReady = File.Exists(nginxExe) && File.Exists(certPem),
                StatusDetail = (File.Exists(nginxExe) ? "Nginx Hazır" : "Nginx Yok") + " | " + (File.Exists(certPem) ? "SSL Hazır" : "SSL Yok")
            });

            // 6. Patchserver + Firewall + Task
            string patchCfg = Path.Combine(ProjectRoot, @"runtime\patchserver\patchserver.json");
            steps.Add(new SetupStepState
            {
                Id = "patchserver",
                Title = "6. Patch Sunucusu, Görev Zamanlayıcı & Güvenlik Duvarı",
                Description = "runtime\\patchserver dağıtımı, VALIANT2-Stack başlangıç görevi ve güvenlik duvarı portları",
                IsReady = File.Exists(patchCfg),
                StatusDetail = File.Exists(patchCfg) ? "Patch Sunucusu Yapılandırıldı" : "Kurulum Gerekli"
            });

            // 7. Database Schemas
            bool dbTablesReady = false;
            if (mariaPort)
            {
                string err;
                string res = RunSqlQuery("SHOW DATABASES LIKE 'player';", null, out err);
                dbTablesReady = string.IsNullOrEmpty(err) && res.Contains("player");
            }
            steps.Add(new SetupStepState
            {
                Id = "database",
                Title = "7. Oyun & Panel Veritabanı Şemaları (SQL Import)",
                Description = "account, common, log, player (bootstrap + extra_tables + drop_seed) ve valiant_panel kurulumu",
                IsReady = dbTablesReady,
                StatusDetail = dbTablesReady ? "Veritabanları & Tablolar Hazır" : "İçe Aktarım Gerekli"
            });

            // 8. Symlinks & Config Sync
            string turkeyDir = Path.Combine(ProjectRoot, @"runtime\server\main\srv1\share\locale\turkey");
            steps.Add(new SetupStepState
            {
                Id = "symlinks",
                Title = "8. Symlink/Junction Onarımı & Config Senkronizasyonu",
                Description = "Windows/Linux symlink referans dosyalarını (CMD, CRC, VERSION, data, locale) ve CONFIG dosyalarını onarır",
                IsReady = Directory.Exists(turkeyDir),
                StatusDetail = Directory.Exists(turkeyDir) ? "Junction & Config Hazır" : "Senkronizasyon Gerekli"
            });

            // 9. Binaries & Packs
            bool hasGameExe = File.Exists(Path.Combine(ProjectRoot, @"runtime\server\main\srv1\share\bin\game.exe"));
            bool hasClientExe = File.Exists(Path.Combine(ProjectRoot, @"runtime\client\game\bin\M2Client.exe"));
            bool hasRootPak = File.Exists(Path.Combine(ProjectRoot, @"runtime\client\game\pack\root.pak"));
            bool hasPatcher = File.Exists(Path.Combine(ProjectRoot, @"runtime\client\VALIANT2.exe"));
            steps.Add(new SetupStepState
            {
                Id = "build",
                Title = "9. Sunucu, İstemci, Packler ve Autopatcher Derlemesi",
                Description = "game.exe, db.exe, M2Client.exe, config.exe, tüm .pak dosyaları ve VALIANT2.exe derlenir",
                IsReady = hasGameExe && hasClientExe && hasRootPak && hasPatcher,
                StatusDetail = string.Format("Server:{0} | Client:{1} | Pack:{2} | Patcher:{3}",
                    hasGameExe ? "OK" : "Yok", hasClientExe ? "OK" : "Yok", hasRootPak ? "OK" : "Yok", hasPatcher ? "OK" : "Yok")
            });

            return steps;
        }

        public List<PackEntryInfo> GetPackEntries()
        {
            var result = new List<PackEntryInfo>();
            string cfgPath = Path.Combine(ProjectRoot, @"assets\unpacked\config.json");
            if (!File.Exists(cfgPath)) return result;

            string content = File.ReadAllText(cfgPath, Encoding.UTF8);
            var matches = Regex.Matches(content, @"""dir""\s*:\s*""([^""]+)""\s*,\s*""file""\s*:\s*""([^""]+)""");
            foreach (Match m in matches)
            {
                string dir = m.Groups[1].Value; // e.g. data/root
                string fileRel = m.Groups[2].Value; // e.g. ../../runtime/client/game/pack/root.pak
                string packName = dir.StartsWith("data/") ? dir.Substring(5) : dir;
                string fullPak = Path.GetFullPath(Path.Combine(ProjectRoot, @"assets\unpacked", fileRel.Replace('/', '\\')));
                var fi = new FileInfo(fullPak);
                result.Add(new PackEntryInfo
                {
                    Name = packName,
                    SourceDir = dir,
                    PakFile = Path.GetFileName(fullPak),
                    Exists = fi.Exists,
                    SizeBytes = fi.Exists ? fi.Length : 0,
                    LastModified = fi.Exists ? fi.LastWriteTime : DateTime.MinValue
                });
            }
            return result;
        }

        public void EmitLog(string text, bool isError = false)
        {
            var handler = OnOutputLine;
            if (handler != null) handler(text, isError);
        }

        public void StopActiveCommand()
        {
            lock (procLock)
            {
                if (activeProcess != null && !activeProcess.HasExited)
                {
                    try
                    {
                        Process.Start(new ProcessStartInfo
                        {
                            FileName = "taskkill.exe",
                            Arguments = "/F /T /PID " + activeProcess.Id,
                            CreateNoWindow = true,
                            UseShellExecute = false
                        }).WaitForExit(3000);
                    }
                    catch { }
                    EmitLog("[!] İşlem kullanıcı tarafından durduruldu.", true);
                }
            }
        }

        public Task<int> RunPowerShellScriptAsync(string taskTitle, string scriptName, string arguments = "")
        {
            string scriptPath = Path.Combine(ScriptsDir, scriptName);
            string body = string.Format(
                "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8; & '{0}' {1}",
                scriptPath.Replace("'", "''"), arguments);
            return RunPowerShellInlineAsync(taskTitle, body);
        }

        public Task<int> RunPowerShellInlineAsync(string taskTitle, string psCommand)
        {
            string tempScript = Path.Combine(Path.GetTempPath(), "valiant2_task_" + Guid.NewGuid().ToString("N") + ".ps1");
            string header = "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8\r\n$OutputEncoding = [System.Text.Encoding]::UTF8\r\n$ErrorActionPreference = 'Stop'\r\n";
            File.WriteAllText(tempScript, header + psCommand, new UTF8Encoding(true));
            string psArgs = string.Format("-NoProfile -NonInteractive -ExecutionPolicy Bypass -File \"{0}\"", tempScript);
            return RunProcessAsync(taskTitle, "powershell.exe", psArgs, ProjectRoot, () =>
            {
                try { File.Delete(tempScript); } catch { }
            });
        }

        public Task<int> RunProcessAsync(string taskTitle, string fileName, string arguments, string workingDir = null, Action cleanup = null)
        {
            return Task.Run(() =>
            {
                lock (procLock)
                {
                    if (activeProcess != null && !activeProcess.HasExited)
                    {
                        EmitLog("[!] Şu anda çalışan başka bir işlem var. Lütfen bitmesini bekleyin veya durdurun.", true);
                        return -1;
                    }
                }

                var stateHandler = OnTaskStateChanged;
                if (stateHandler != null) stateHandler(taskTitle, true);

                var sw = Stopwatch.StartNew();
                EmitLog("======================================================================", false);
                EmitLog(string.Format("[{0:HH:mm:ss}] BAŞLATILDI: {1}", DateTime.Now, taskTitle), false);
                EmitLog("----------------------------------------------------------------------", false);

                int exitCode = -1;
                try
                {
                    var psi = new ProcessStartInfo
                    {
                        FileName = fileName,
                        Arguments = arguments,
                        WorkingDirectory = string.IsNullOrEmpty(workingDir) ? ProjectRoot : workingDir,
                        UseShellExecute = false,
                        RedirectStandardInput = true,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        CreateNoWindow = true,
                        StandardOutputEncoding = Encoding.UTF8,
                        StandardErrorEncoding = Encoding.UTF8
                    };

                    var proc = new Process { StartInfo = psi, EnableRaisingEvents = true };
                    proc.OutputDataReceived += (s, e) => { if (e.Data != null) EmitLog(e.Data, false); };
                    proc.ErrorDataReceived += (s, e) => { if (e.Data != null) EmitLog(e.Data, true); };

                    lock (procLock) { activeProcess = proc; }
                    proc.Start();
                    try { proc.StandardInput.Close(); } catch { }
                    proc.BeginOutputReadLine();
                    proc.BeginErrorReadLine();
                    proc.WaitForExit();
                    exitCode = proc.ExitCode;
                }
                catch (Exception ex)
                {
                    EmitLog("[HATA] " + ex.Message, true);
                }
                finally
                {
                    lock (procLock) { activeProcess = null; }
                    if (cleanup != null) cleanup();
                    sw.Stop();
                    if (exitCode == 0)
                        EmitLog(string.Format("[{0:HH:mm:ss}] TAMAMLANDI: {1} ({2:0.0} sn)", DateTime.Now, taskTitle, sw.Elapsed.TotalSeconds), false);
                    else
                        EmitLog(string.Format("[{0:HH:mm:ss}] SONUÇLANDI (Kod: {1}): {2} ({3:0.0} sn)", DateTime.Now, exitCode, taskTitle, sw.Elapsed.TotalSeconds), true);

                    if (stateHandler != null) stateHandler(taskTitle, false);
                }
                return exitCode;
            });
        }
    }
}
