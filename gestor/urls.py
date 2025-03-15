from django.urls import path
from .views import *

#rutas de la aplicacion "gestor"
urlpatterns = [
    path('', home), # vacio es igual a / (raiz)
    path('create', createAlumno),
    path('update', updateAulmno),
    path('delete', deleteAlumno)
]
