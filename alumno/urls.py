from django.urls import path
from .views import *

#rutas de la aplicacion alumno
urlpatterns = [
    path("",login_view),
    path('logout/',logout_view),
    path('alumno/miinfo/',cliente_index),
    path('alumno/history/',cliente_history),
    path('alumno/payment/',cliente_payment),
    path('alumno/checkout/',checkout_session),
    path('stripe/webhook',stripe_webhook)
]
