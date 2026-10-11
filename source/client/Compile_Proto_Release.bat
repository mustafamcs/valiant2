@echo off
CALL "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat"
cd %~dp0
msbuild ..\OtherTools\DumpProto\DumpProto.sln /property:Configuration=Release /maxcpucount
pause
