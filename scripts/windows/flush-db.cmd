@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ". '%~dp0common.ps1'; Flush-ServerDatabaseCaches; Write-Host 'Tum kanallara @FLUSH_SAVE gonderildi ve DB onbellekleri diske yazildi.' -ForegroundColor Green"
