@echo off
REM Activar entorno y ejecutar servidor Django en una ventana
start cmd /k "call entorno_web\Scripts\activate && python manage.py runserver"

REM Activar entorno y ejecutar Stripe listener en otra ventana
start cmd /k "call entorno_web\Scripts\activate && .\stripe\stripe listen --forward-to localhost:8000/stripe/webhook/"

echo Servidor Django y Stripe Listener iniciados en paralelo.
pause