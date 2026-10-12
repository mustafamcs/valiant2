@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0create-account.ps1" %*
exit /b %errorlevel%
