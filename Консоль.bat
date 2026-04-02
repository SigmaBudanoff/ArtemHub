@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo [1/2] Очищення старих файлів...
rd /s /q build dist 2>nul

echo [2/2] Створення EXE (Artemis OS)...
:: Ми просто додаємо всю папку assets цілком
py -m PyInstaller --noconsole --onefile --add-data "assets;assets" Artemis_OS.py

echo.
echo ПЕРЕМОГА! Файл Artemis_OS.exe створено в папці dist.
echo Не забудьте, що папка 'assets' має бути поруч із ним!
pause
exit
