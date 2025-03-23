from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Plan, Cliente
from .forms import registerClient, loginForm
from .enums import Headers, DatabaseColumns

# Create your views here.
#proteccion contra no autenticacion
@login_required
def index(request):
    print(request.user)
    print(request.user.is_authenticated)
    return render(request,'indexClient.html',{
        "context":"Alumnos",
        "headers_pln": Headers.PLANHEADERS,
        "plans": Plan.objects.all(),
        "headers_alu": Headers.ALUMNOHEADERS,
        "clients":Cliente.objects.all()
    })

@login_required
def createAlumno(request):
    #peticion get renderiza la pagina
    if request.method == "GET":
        return render(request,'createClient.html',{
            "context":"Registrar alumno",
            "form":registerClient()
        })
    else:
        #guardar datos en la base de datos
        Cliente.objects.create(curp=request.POST[DatabaseColumns.ALUMNOCOLUMNS[0]],
                               nombre=request.POST[DatabaseColumns.ALUMNOCOLUMNS[1]],
                               direccion=request.POST[DatabaseColumns.ALUMNOCOLUMNS[2]],
                               telefono=request.POST[DatabaseColumns.ALUMNOCOLUMNS[3]],
                               correo=request.POST[DatabaseColumns.ALUMNOCOLUMNS[4]],
                               fecha_nac=request.POST[DatabaseColumns.ALUMNOCOLUMNS[5]],
                               id_plan=Plan.objects.get(id_plan=request.POST[DatabaseColumns.ALUMNOCOLUMNS[6]])
                               )
        return redirect("/alumno/")
@login_required
def updateAulmno(request):
    return render(request,'updateClient.html',{'context':'Modificar alumno'})

@login_required
def deleteAlumno(request):
    return render(request,'deleteClient.html',{'context':'Eliminar alumno'})

@login_required
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

#formulario de login
def login_view(request):
    #instancia de formulario
    form = loginForm()
    #validamos el metodo
    if request.method == "POST":
        user = authenticate(username=request.POST['user'],password=request.POST['password'])
        if user:
            login(request, user)
            return redirect("/alumno/")
        else:
            return render(request,'login.html',{'context':'Login','error':'Usuario o contraseña incorrectos','form':form})#renderizar plantilla
    return render(request,'login.html',{'context':'Login','error':'','form':form})#renderizar plantilla