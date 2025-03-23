from django import forms
from django.contrib.auth import authenticate
from .models import Plan

#clase de formulario de registro
class registerClient(forms.Form):
    #campos del formulario
    curp = forms.CharField(label="CURP:",
                           max_length=18,
                           widget=forms.TextInput(attrs={"style":"float: right;"}))
    nombre = forms.CharField(label="Nombre completo: ",
                             max_length=80,
                             widget=forms.TextInput(attrs={"style":"float: right;"}))
    direccion = forms.CharField(label="Direccion:",
                                max_length=60,
                                widget=forms.TextInput(attrs={"style":"float: right;"}))
    telefono = forms.CharField(label="Telefono:",
                               max_length=12,
                               widget=forms.TextInput(attrs={"style":"float: right;"}))
    correo = forms.EmailField(label="Correo electronico:",
                              max_length=30,
                              widget=forms.EmailInput(attrs={"style":"float: right;"}))
    fecha_nac = forms.DateField(label="Fecha de nacimiento:",
                                widget=forms.DateInput(attrs={"style":"float: right;"}))
    id_plan = forms.ModelChoiceField(queryset=Plan.objects.all(),
                                     widget=forms.Select(attrs={"style":"float: right;"}))#id de modelos

#clase de formulario de login
class loginForm(forms.Form):
    #campos del formulario
    user = forms.CharField(label="Nombre de usuario:",
                           max_length=20,
                           widget=forms.TextInput(attrs={"style":"float: right;"}))
    password = forms.CharField(label="Contraseña:",
                               max_length=20,
                               widget=forms.PasswordInput(attrs={"style":"float: right;"}))