using System;
using System.Runtime.InteropServices;
using System.Windows.Forms;

namespace Valiant2ControlCenter
{
    internal static class Program
    {
        [DllImport("user32.dll")]
        private static extern bool SetProcessDPIAware();

        [STAThread]
        private static void Main(string[] args)
        {
            try { SetProcessDPIAware(); } catch { }
            string captureDir = null;
            bool runE2e = false;
            if (args != null && args.Length >= 2 && args[0] == "--capture-pages")
            {
                captureDir = args[1];
            }
            else if (args != null && args.Length >= 2 && args[0] == "--run-e2e-test")
            {
                runE2e = true;
                captureDir = args[1];
            }

            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new ControlCenterForm(captureDir, runE2e));
        }
    }
}
