from django.contrib import admin
from .models import Plan, Pago, Cliente

# Register your models here.
admin.site.register(Plan)
admin.site.register(Pago)
admin.site.register(Cliente)