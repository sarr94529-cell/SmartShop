@echo off
cd /d "%~dp0"
echo Installation SmartShop...
if not exist env\Scripts\python.exe (py -3 -m venv env)
if errorlevel 1 (echo ERREUR: Python est requis. & pause & exit /b 1)
call env\Scripts\activate.bat
python -m pip install -r requirements.txt
if errorlevel 1 (echo ERREUR pendant l'installation. & pause & exit /b 1)
if not exist .env copy .env.example .env
python manage.py makemigrations boutique analytics
if errorlevel 1 (pause & exit /b 1)
python manage.py migrate
if errorlevel 1 (pause & exit /b 1)
python manage.py produits_demo
if errorlevel 1 (pause & exit /b 1)
python manage.py check
if errorlevel 1 (pause & exit /b 1)
echo.
echo Ouvrez http://127.0.0.1:8000/ apres demarrage.
echo Pour creer un administrateur: python manage.py createsuperuser
echo.
python manage.py runserver
pause
