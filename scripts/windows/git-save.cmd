@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0git-save.ps1" %*
exit /b %errorlevel%
