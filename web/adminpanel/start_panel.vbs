Set sh = CreateObject("WScript.Shell")
php = "C:\Users\Administrator\AppData\Local\Microsoft\WinGet\Packages\PHP.PHP.8.3_Microsoft.Winget.Source_8wekyb3d8bbwe\php.exe"
dirp = "C:\Users\Administrator\Desktop\VALIANT2\web\adminpanel"
ports = Array(8090, 8092, 8093, 8094)
For Each p In ports
    sh.Run "cmd /c cd /d " & dirp & " && """ & php & """ -d display_errors=0 -S 127.0.0.1:" & p & " router.php", 0, False
Next
