@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0stack-status.ps1" %*
exit /b %errorlevel%
