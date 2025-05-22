from django import forms

# Formulario de registro de cliente
class registerClient(forms.Form):
    curp = forms.CharField(label="CURP:", max_length=18, widget=forms.TextInput(attrs={"style": "float: right;", "placeholder": "curp (18 digs)"}))
    nombre = forms.CharField(label="Nombre completo:", max_length=80, widget=forms.TextInput(attrs={"style": "float: right;", "placeholder": "john doe"}))
    direccion = forms.CharField(label="Dirección:", max_length=60, widget=forms.TextInput(attrs={"style": "float: right;", "placeholder": "Somewhere #100"}))
    telefono = forms.CharField(label="Teléfono:", max_length=12, widget=forms.TextInput(attrs={"style": "float: right;", "placeholder": "477#######"}))
    correo = forms.EmailField(label="Correo electrónico:", max_length=30, widget=forms.EmailInput(attrs={"style": "float: right;", "placeholder": "jdoe@gmail.com"}))
    fecha_nac = forms.DateField(label="Fecha de nacimiento:", widget=forms.DateInput(attrs={"style": "float: right;", "placeholder": "YYYY-MM-DD"}))
    curp_familiar = forms.CharField(label="CURP de familiar (opcional):", max_length=18, required=False, widget=forms.TextInput(attrs={"style": "float: right;", "placeholder": "curp (18 digs)"}))

# Formulario de login
class loginForm(forms.Form):
    user = forms.CharField(label="Nombre de usuario:", max_length=20, widget=forms.TextInput(attrs={"style": "float: right;"}))
    password = forms.CharField(label="Contraseña:", max_length=20, widget=forms.PasswordInput(attrs={"style": "float: right;"}))

# Formulario de búsqueda por nombre
class searchClient(forms.Form):
    nombre = forms.CharField(label="Nombre del alumno", max_length=80, widget=forms.TextInput(attrs={"placeholder": "nombre completo"}))

# Formulario de búsqueda por CURP
class searchClientByCurp(forms.Form):
    curp = forms.CharField(label="CURP del alumno:", max_length=18, widget=forms.TextInput(attrs={"style": "float: right;", "placeholder": "CURP (18 digs)"}))

# Formulario para actualizar alumno
class updateClientForm(forms.Form):
    nombre = forms.CharField(label="Nombre completo:", max_length=80, widget=forms.TextInput(attrs={"style": "float: right;", "placeholder": "john doe"}))
    direccion = forms.CharField(label="Dirección:", max_length=60, widget=forms.TextInput(attrs={"style": "float: right;", "placeholder": "Somewhere #100"}))
    telefono = forms.CharField(label="Teléfono:", max_length=12, widget=forms.TextInput(attrs={"style": "float: right;", "placeholder": "477#######"}))
    correo = forms.EmailField(label="Correo electrónico:", max_length=30, widget=forms.EmailInput(attrs={"style": "float: right;", "placeholder": "jdoe@gmail.com"}))
    fecha_nac = forms.DateField(label="Fecha de nacimiento:", widget=forms.DateInput(attrs={"style": "float: right;", "placeholder": "YYYY-MM-DD"}))
    curp_familiar = forms.CharField(label="CURP de familiar (opcional):", max_length=18, required=False, widget=forms.TextInput(attrs={"style": "float: right;", "placeholder": "curp (18 digs)"}))
    es_plan_familiar = forms.BooleanField(label="Plan familiar", required=False)

# Formulario de registro de pago
class registerPaymentForm(forms.Form):
    monto = forms.DecimalField(label="Monto:", max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={"style": "float: right;", "readonly": "readonly"}))
    fecha_pago = forms.DateField(label="Fecha de pago:", widget=forms.DateInput(attrs={"style": "float: right;", "type": "date"}))
    tipo = forms.ChoiceField(label="Forma de pago:", choices=[('Efectivo', 'Efectivo')], widget=forms.Select(attrs={"style": "float: right;"}))
    retrasado = forms.BooleanField(label="¿Pago con retraso?", required=False)
