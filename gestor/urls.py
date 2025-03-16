from django.urls import path
from .views import *

#rutas de la aplicacion "gestor"
urlpatterns = [
    path('', login),
    path('alumno/', index), # vacio es igual a / (raiz)
    path('alumno/create', createAlumno),
    path('alumno/update', updateAulmno),
    path('alumno/delet', deleteAlumno),
    path('plan/<str:id_pl>', showPlan)#ruta con parametro
]
