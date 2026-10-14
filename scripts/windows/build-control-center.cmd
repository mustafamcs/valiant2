@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build-control-center.ps1" %*
