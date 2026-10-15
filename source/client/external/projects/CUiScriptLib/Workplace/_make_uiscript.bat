@echo off
pushd "%~dp0"
if not exist "UiScriptLib" mkdir "UiScriptLib"
if exist "..\..\..\lib\uiscriptlib.lib" if exist "UiScriptLib\PythonuiscriptlibManager.cpp" if exist "UiScriptLib\cyTemp\loginwindow.c" (
    powershell -NoProfile -Command "$ref = (Get-Item 'UiScriptLib\PythonuiscriptlibManager.cpp').LastWriteTimeUtc; $newer = Get-ChildItem '..\..\CRootLib\Workplace\__cython\uiscript_modules\*.py' -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTimeUtc -gt $ref } | Select-Object -First 1; if ($newer) { exit 1 } else { exit 0 }"
    if not errorlevel 1 (
        echo CUiScriptLib up-to-date, skipping cythonizer.
        popd
        exit /b 0
    )
)
if exist "..\..\CRootLib\Workplace\__cython\uiscript_modules\*.py" (
    copy /y "..\..\CRootLib\Workplace\__cython\uiscript_modules\*.py" "UiScriptLib\" >nul
    echo copy completed
) else (
    echo __cython not found, using existing UiScriptLib sources
)

cd UiScriptLib\
C:\Python27\python.exe UiScriptLibCythonizer.py
set EXIT_CODE=%ERRORLEVEL%
if %EXIT_CODE%==0 powershell -NoProfile -Command "(Get-Item 'PythonuiscriptlibManager.cpp').LastWriteTimeUtc = [DateTime]::UtcNow"
popd
exit /b %EXIT_CODE%
