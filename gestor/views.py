from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Plan, Cliente
from .forms import registerClient
from .enums import Headers

# Create your views here.
def index(request):
    return render(request,'indexClient.html',{
        "context":"Alumnos",
        "headers": Headers.ALUMNOHEADERS,
        "clients":Cliente.objects.all()
    })

def createAlumno(request):
    #peticion get renderiza la pagina
    if request.method == "GET":
        return render(request,'createClient.html',{
            "context":"Registrar alumno",
            "form":registerClient()
        })
    else:
        #guardar datos en la base de datos
        Cliente.objects.create(curp=request.POST['curp'],
                               nombre=request.POST['nombre'],
                               direccion=request.POST['direccion'],
                               telefono=request.POST['telefono'],
                               correo=request.POST['correo'],
                               fecha_nac=request.POST['fecha_nac'],
                               id_plan=Plan.objects.get(id_plan=request.POST['id_plan'])
                               )
        return redirect("/alumno/")

def updateAulmno(request):
    return HttpResponse("<h1>Cambiar datos de alumno</h1>")

def deleteAlumno(request):
    return HttpResponse("<h1>Eliminar alumno</h1>")

def showPlan(request, id_pl):
    #en caso de que no se encuentre el recurso
    plan = get_object_or_404(Plan, id_plan=id_pl)
    return render(request,'planInfo.html',{
        'context':f'Info {plan.id_plan}',
        'id_pl':plan.id_plan,
        'nombre_pl':plan.nombre_pl,
        'mensualidad':plan.mensualidad,
        'inscripcion':plan.inscripcion
    })#plantilla con parametros

def login(request):
    return render(request,'login.html',{'context':'Login'})#renderizar plantilla