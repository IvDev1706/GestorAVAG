from django import forms

#clase de formulario de registro
class registerClient(forms.Form):
    #campos del formulario
    curp = forms.CharField(label="CURP:",
                           max_length=18,
                           widget=forms.TextInput(attrs={"style":"float: right;",
                                                         "placeholder":"curp (18 digs)"}))
    nombre = forms.CharField(label="Nombre completo: ",
                             max_length=80,
                             widget=forms.TextInput(attrs={"style":"float: right;",
                                                           "placeholder":"john doe"}))
    direccion = forms.CharField(label="Direccion:",
                                max_length=60,
                                widget=forms.TextInput(attrs={"style":"float: right;",
                                                              "placeholder": "Somewhere #100"}))
    telefono = forms.CharField(label="Telefono:",
                               max_length=12,
                               widget=forms.TextInput(attrs={"style":"float: right;",
                                                             "placeholder":"477#######"}))
    correo = forms.EmailField(label="Correo electronico:",
                              max_length=30,
                              widget=forms.EmailInput(attrs={"style":"float: right;",
                                                             "placeholder":"jdoe@gmail.com"}))
    fecha_nac = forms.DateField(label="Fecha de nacimiento:",
                                widget=forms.DateInput(attrs={"style":"float: right;",
                                                              "placeholder":"YYYY-MM-DD"}))
    curp_familiar = forms.CharField(label="CURP de familiar (opcional):",
                                    max_length=18,
                                    required=False,
                                    widget=forms.TextInput(attrs={"style":"float: right;",
                                                                  "placeholder":"curp (18 digs)"}))

#clase de formulario de login
class loginForm(forms.Form):
    #campos del formulario
    user = forms.CharField(label="Nombre de usuario:",
                           max_length=20,
                           widget=forms.TextInput(attrs={"style":"float: right;"}))
    password = forms.CharField(label="Contraseña:",
                               max_length=20,
                               widget=forms.PasswordInput(attrs={"style":"float: right;"}))

#clase de formulario de busqueda por nombre
class searchClient(forms.Form):
    #campos del formulario
    nombre = forms.CharField(label="Nombre del alumno",
                             max_length=80,
                             widget=forms.TextInput(attrs={"placeholder":"nombre completo"}))