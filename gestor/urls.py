from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

#rutas de la aplicacion "gestor"
urlpatterns = [
    path('',login_view),
    path('logout/view', logout_view),
    path('logout/', LogoutView.as_view()),
    path('alumno/', index), # vacio es igual a / (raiz)
    path('alumno/create', createAlumno),
    path('alumno/update', updateAulmno),
    path('alumno/delete', deleteAlumno),
    path('pago/register',createPago),
    path('pago/history/<str:curp>/', historyPago)
]
