#clase de enums
class Headers:
    #encabezados de alumno
    ALUMNOHEADERS = ["Curp","Nombre completo","Direccion","Telefono","Correo","Fecha de nacimiento","Tipo de plan"]
    #ecabezados de plan
    PLANHEADERS = ["Id plan","Nombre","Mensualidad (MXN)","Inscripcion (MXN)"]
    #encabezados de pago
    PAGOHEADERS = ["Id de pago","Monto","Fecha de pago","Forma de pago","Retraso"]

class DatabaseColumns:
    #columnas de alumno
    ALUMNOCOLUMNS = ["curp","nombre","direccion","telefono","correo","fecha_nac","id_plan"]
    #columnas de Plan
    PLANCOLUMNS = ["id_plan","nombre_pl","mensualidad","inscripcion"]
    #columnas de pago
    PAGOCOLUMNS = ["id_pago","monto","fecha_pago","tipo","retrasado","curp"]