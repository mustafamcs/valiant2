@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0build-client-packs.ps1" %*
exit /b %errorlevel%
