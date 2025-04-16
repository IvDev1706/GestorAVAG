from django.urls import path
from .views import *

#rutas de la aplicacion alumno
urlpatterns = [
    path("",login_view),
    path('logout/',logout_view),
    path('alumno/miinfo/',cliente_index)
]
