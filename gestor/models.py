from django.db import models

# Create your models here.
class Plan(models.Model):
    #campos de la tabla
    id_plan = models.CharField(max_length=3,primary_key=True, null=False)
    nombre_pl = models.CharField(max_length=20,null=False)
    mensualidad = models.DecimalField(decimal_places=2, null=False, max_digits=10)
    inscripcion = models.DecimalField(decimal_places=2, null=False, max_digits=10)
    
    #substring
    def __str__(self):
        return self.id_plan
    
class Cliente(models.Model):
    #campos de la tabla
    curp = models.CharField(max_length=18, primary_key=True, null=False)
    nombre = models.CharField(max_length=80, null=False)
    direccion = models.CharField(max_length=60, null=False)
    telefono = models.CharField(max_length=12, null=False)
    correo = models.CharField(max_length=30, null=False)
    fecha_nac = models.DateField(null=False)
    #relacion
    id_plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.curp
    
class Pago(models.Model):
    #campos de la tabla
    id_pago = models.AutoField(primary_key=True)
    monto = models.DecimalField(decimal_places=2, null=False, max_digits=10)
    fecha_pago = models.DateField(null=False)
    tipo = models.CharField(max_length=20, null=False)
    retrasado = models.BooleanField(null=False)
    curp = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.id_pago