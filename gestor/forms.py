from django import forms
from django.contrib.auth import authenticate
from .models import Plan

#clase de formulario de registro
class registerClient(forms.Form):
    #campos del formulario
    curp = forms.CharField(label="CURP:",max_length=18)
    nombre = forms.CharField(label="Nombre completo: ",max_length=80)
    direccion = forms.CharField(label="Direccion:",max_length=60)
    telefono = forms.CharField(label="Telefono:",max_length=12)
    correo = forms.EmailField(label="Correo electronico:",max_length=30)
    fecha_nac = forms.DateField(label="Fecha de nacimiento:")
    id_plan = forms.ModelChoiceField(queryset=Plan.objects.all())#id de modelos

#clase de formulario de login
class loginForm(forms.Form):
    #campos del formulario
    user = forms.CharField(label="Nombre de usuario:",max_length=20)
    password = forms.CharField(label="Contraseña:",max_length=20,widget=forms.PasswordInput)