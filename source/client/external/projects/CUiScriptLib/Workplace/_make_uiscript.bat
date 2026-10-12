@echo off
pushd "%~dp0"
if not exist "UiScriptLib" mkdir "UiScriptLib"
if exist "..\..\CRootLib\Workplace\__cython\uiscript_modules\*.py" (
    copy /y "..\..\CRootLib\Workplace\__cython\uiscript_modules\*.py" "UiScriptLib\"
    echo copy completed
) else (
    echo __cython not found, using existing UiScriptLib sources
)

cd UiScriptLib\
C:\Python27\python.exe UiScriptLibCythonizer.py
set EXIT_CODE=%ERRORLEVEL%
popd
exit /b %EXIT_CODE%
