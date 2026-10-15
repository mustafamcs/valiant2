@echo off
pushd "%~dp0"
if not exist "RootLib" mkdir "RootLib"
if exist "..\..\..\lib\rootlib.lib" if exist "RootLib\PythonrootlibManager.cpp" if exist "RootLib\cyTemp\serverInfo.c" (
    powershell -NoProfile -Command "$ref = (Get-Item 'RootLib\PythonrootlibManager.cpp').LastWriteTimeUtc; $newer = Get-ChildItem '__cython\root_modules\*.py' -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTimeUtc -gt $ref } | Select-Object -First 1; if ($newer) { exit 1 } else { exit 0 }"
    if not errorlevel 1 (
        echo CRootLib up-to-date, skipping cythonizer.
        popd
        exit /b 0
    )
)
if exist "__cython\root_modules\*.py" (
    copy /y "__cython\root_modules\*.py" "RootLib\" >nul
    echo copy completed
) else (
    echo __cython not found, using existing RootLib sources
)

cd RootLib\
C:\Python27\python.exe RootLibCythonizer.py
set EXIT_CODE=%ERRORLEVEL%
if %EXIT_CODE%==0 powershell -NoProfile -Command "(Get-Item 'PythonrootlibManager.cpp').LastWriteTimeUtc = [DateTime]::UtcNow"
popd
exit /b %EXIT_CODE%
