@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo [1/3] Очищення старих збірок...
if exist "Artemis_OS.exe" del /f /q "Artemis_OS.exe"
rd /s /q build dist 2>nul

echo [2/3] Створення EXE (зачекайте)...
:: Збираємо ОДНИМ файлом, але НЕ вшиваємо assets всередину (так надійніше)
py -m PyInstaller --noconsole --onefile Artemis_OS.py

echo [3/3] Перенесення файлу та прибирання...
if exist "dist\Artemis_OS.exe" (
    move /y "dist\Artemis_OS.exe" .
    rd /s /q build dist 2>nul
    del /f /q *.spec 2>nul
    echo СИСТЕМА ГОТОВА! Запускайте Artemis_OS.exe поруч із папкою assets.
) else (
    echo ПОМИЛКА: EXE не було створено. Перевірте помилки в консолі.
)

pause
exit
