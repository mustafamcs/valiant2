@echo off
call "%~dp0stop-server.cmd"
call "%~dp0start-server.cmd" %*
exit /b %errorlevel%
