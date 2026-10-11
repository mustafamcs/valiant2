using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

namespace Valiant2Launcher
{
    internal static class Program
    {
        [STAThread]
        private static void Main(string[] args)
        {
            if (args.Length == 1 && (args[0] == "--play" || args[0] == "--config"))
            {
                var game = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "game");
                var target = Path.Combine(game, args[0] == "--play" ? "M2Client.exe" : "config.exe");
                if (File.Exists(target)) Process.Start(new ProcessStartInfo(target) { WorkingDirectory = game, UseShellExecute = true });
                return;
            }
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new LauncherForm());
        }
    }
}
