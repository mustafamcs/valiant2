using System;
using System.IO;
using System.Windows.Forms;

namespace Valiant2Config
{
    internal static class Program
    {
        [STAThread]
        private static int Main(string[] args)
        {
            if (args.Length > 0)
            {
                try
                {
                    var config = ClientConfig.Load(args.Length > 1 ? args[1] : "metin2.cfg");
                    if (args[0] == "--validate")
                        return config.Validate() ? 0 : 1;
                    if (args[0] == "--roundtrip" && args.Length > 2)
                    {
                        config.Save(args[2]);
                        return ClientConfig.Load(args[2]).Validate() ? 0 : 1;
                    }
                }
                catch (Exception ex)
                {
                    Console.Error.WriteLine(ex.Message);
                    return 1;
                }
            }

            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new ConfigForm(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "metin2.cfg")));
            return 0;
        }
    }
}
