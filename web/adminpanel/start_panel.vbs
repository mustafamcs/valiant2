Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
dirp = fso.GetParentFolderName(WScript.ScriptFullName)
root = fso.GetParentFolderName(fso.GetParentFolderName(dirp))
psScript = root & "\scripts\windows\start-stack.ps1"
sh.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & psScript & """", 0, False
