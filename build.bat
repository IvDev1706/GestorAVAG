@echo off
python -m venv entorno_web
call entorno_web\scripts\activate
pip install django
pip install mysqlclient
pip install stripe
echo entorno creado
pause 