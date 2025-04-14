from django import forms

#formulario de login
class LoginForm(forms.Form):
    #campos del formulario
    curp = forms.CharField(label="Ingrese su curp:",
                           max_length=18,
                           widget=forms.TextInput(attrs={"style":"float: right;"}))