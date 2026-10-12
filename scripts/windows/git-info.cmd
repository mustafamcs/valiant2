@echo off
cd /d "%~dp0..\.."
echo === BRANCH / DURUM ===
git status -sb
echo.
echo === SON 10 COMMIT ===
git log --oneline -10
