@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build-quests.ps1" %*
