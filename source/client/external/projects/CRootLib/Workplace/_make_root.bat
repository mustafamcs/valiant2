@echo off
pushd "%~dp0"
if not exist "RootLib" mkdir "RootLib"
copy /y "__cython\root_modules\*.py" "RootLib\"
echo copy completed

cd RootLib\
C:\Python27\python.exe RootLibCythonizer.py
set EXIT_CODE=%ERRORLEVEL%
popd
exit /b %EXIT_CODE%
