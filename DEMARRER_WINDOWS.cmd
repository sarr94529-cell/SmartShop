@echo off
cd /d "%~dp0"
if not exist env\Scripts\activate.bat (echo Lancez INSTALLER_WINDOWS.cmd d'abord. & pause & exit /b 1)
call env\Scripts\activate.bat
python manage.py runserver
pause
