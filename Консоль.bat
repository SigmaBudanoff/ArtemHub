@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo [1/3] Очищення...
rd /s /q build dist 2>nul
echo [2/3] Збірка НОВОГО файлу в папку dist...
py -m PyInstaller --noconsole --onefile -n Artemis_NEW --add-data "alarm.wav;." --add-data "clock_icon.png;." --add-data "translator_icon.png;." --add-data "qr_icon.png;." --add-data "weather_icon.png;." --add-data "calc_icon.png;." --add-data "report_icon.png;." --add-data "cosmos_icon.png;." --add-data "paint_icon.png;." Artemis_OS.py
echo [3/3] Готово!
del /f /q *.spec 2>nul
exit