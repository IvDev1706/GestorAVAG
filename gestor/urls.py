from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import*


urlpatterns = [
    path('', login_view),
    path('logout/view', logout_view),
    path('logout/', LogoutView.as_view()),
    path('alumno/', index),
    path('alumno/create', createAlumno),
    path('alumno/update', updateAlumno),
    path('alumno/delet', deleteAlumno),
    path('pago/register', createPago),
    path('pago/history/<str:curp>/', historyPago),
    
    # Nuevas rutas con nombres
    path('alumno/update/buscar', buscar_alumno, name='buscar_alumno'),
    path('alumno/update/<str:curp>/', actualizar_alumno, name='actualizar_alumno'),
    path('alumno/delet/buscar', buscar_alumno_eliminar, name='buscar_alumno_eliminar'),
    path('alumno/delet/<str:curp>/', eliminar_alumno, name='eliminar_alumno'),
    path('pago/register/buscar', buscar_alumno_pago, name='buscar_alumno_pago'),
    path('pago/register/<str:curp>/', registrar_pago, name='registrar_pago'),
]
