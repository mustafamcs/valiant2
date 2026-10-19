@echo off
setlocal
set PY=C:\Python27\python.exe

if not exist "%PY%" (
    echo [error] Python 2.7 not found at %PY%
    exit /b 1
)

pushd "%~dp0"

if "%~1"=="" (
    echo Compiling all .py in %CD% recursively...
    "%PY%" -m compileall -q -f .
) else (
    echo Compiling: %~1
    "%PY%" -c "import py_compile,sys; py_compile.compile(sys.argv[1], doraise=True)" "%~1"
)

if errorlevel 1 (
    echo [error] compile failed
    popd
    exit /b 1
)

echo [ok] done
popd
endlocal
