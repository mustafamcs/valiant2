@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0verify-project.ps1" %*
