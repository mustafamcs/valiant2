@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0stop-stack.ps1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0start-stack.ps1"
exit /b %errorlevel%
