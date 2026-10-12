@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0git-sync.ps1" %*
exit /b %errorlevel%
