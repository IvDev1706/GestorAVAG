from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from .models import Plan, Cliente, Pago
from .forms import registerClient, loginForm, searchClient
from .enums import Headers, DatabaseColumns

# Create your views here.
#proteccion contra no autenticacion
@login_required
def index(request):
    if request.method == "GET":
        #paginado de clientes
        all_clients = Cliente.objects.all().order_by(DatabaseColumns.ALUMNOCOLUMNS[0])
        paginador = Paginator(all_clients, 10) # 10 clientes paginados
        page_number = request.GET.get("page")
        clientes = paginador.get_page(page_number)
        
        return render(request,'indexClient.html',{
            "context":"Alumnos",
            "headers_pln": Headers.PLANHEADERS,
            "plans": Plan.objects.all(),
            "form":searchClient(),
            "headers_alu": Headers.ALUMNOHEADERS,
            "clients": clientes
        })
    else:
        #campo__icontains (like), campo__iexact o campo (exacto)
        filtered_clients = Cliente.objects.filter(nombre__icontains=request.POST[DatabaseColumns.ALUMNOCOLUMNS[1]]).order_by(DatabaseColumns.ALUMNOCOLUMNS[0])
        return render(request,'indexClient.html',{
            "context":"Alumnos",
            "headers_pln": Headers.PLANHEADERS,
            "plans": Plan.objects.all(),
            "form":searchClient(),
            "headers_alu": Headers.ALUMNOHEADERS,
            "clients": filtered_clients
        })

@login_required
def createAlumno(request):
    #peticion get renderiza la pagina
    if request.method == "GET":
        return render(request,'createClient.html',{
            "context":"Registrar alumno",
            "form":registerClient(),
            "error":""
        })
    else:
        try:
            try:
                familiar = Cliente.objects.filter(curp=request.POST["curp_familiar"])
                if not familiar.exists():
                    raise Cliente.DoesNotExist
                #validamos que exista el familiar
                familiar.update(id_plan=Plan.objects.get(id_plan="P-F"))
                #guardar datos en la base de datos
                Cliente.objects.create(curp=request.POST[DatabaseColumns.ALUMNOCOLUMNS[0]],
                                    nombre=request.POST[DatabaseColumns.ALUMNOCOLUMNS[1]],
                                    direccion=request.POST[DatabaseColumns.ALUMNOCOLUMNS[2]],
                                    telefono=request.POST[DatabaseColumns.ALUMNOCOLUMNS[3]],
                                    correo=request.POST[DatabaseColumns.ALUMNOCOLUMNS[4]],
                                    fecha_nac=request.POST[DatabaseColumns.ALUMNOCOLUMNS[5]],
                                    id_plan=Plan.objects.get(id_plan="P-F")
                                    )
            except Cliente.DoesNotExist as e:
                print(e)
                #cliente con plan regular
                Cliente.objects.create(curp=request.POST[DatabaseColumns.ALUMNOCOLUMNS[0]],
                                        nombre=request.POST[DatabaseColumns.ALUMNOCOLUMNS[1]],
                                        direccion=request.POST[DatabaseColumns.ALUMNOCOLUMNS[2]],
                                        telefono=request.POST[DatabaseColumns.ALUMNOCOLUMNS[3]],
                                        correo=request.POST[DatabaseColumns.ALUMNOCOLUMNS[4]],
                                        fecha_nac=request.POST[DatabaseColumns.ALUMNOCOLUMNS[5]],
                                        id_plan=Plan.objects.get(id_plan="P-R")
                                        )
                return redirect("/admon/alumno/")
            return redirect("/admon/alumno/")
        #validacion de registro duplicado
        except IntegrityError as e:
            # cliente duplicado
            return render(request,'createClient.html',{
                "context":"Registrar alumno",
                "form":registerClient(),
                "error":"Alumno ya registrado"
            })
    
@login_required
def updateAulmno(request):
    return render(request,'updateClient.html',{'context':'Modificar alumno'})

@login_required
def deleteAlumno(request):
    return render(request,'deleteClient.html',{'context':'Eliminar alumno'})

@login_required
def createPago(request):
    return render(request, 'pagoRegister.html',{'context':'Registrar pago'})

@login_required
def historyPago(request, curp):
    #obtener los pagos del cliente
    all_pays = Pago.objects.filter(curp_id=curp).order_by(DatabaseColumns.PAGOCOLUMNS[2])
    paginador = Paginator(all_pays, 10)
    page = request.GET.get("page")
    if page:
        pays = paginador.page(page)
    else:
        pays = paginador.page(1)
    
    client = Cliente.objects.get(curp=curp).nombre
    return render(request,'history.html',{'context':'Historial de pagos',
                                          'client_curp':curp,
                                          'client_name':client,
                                          'headers':Headers.PAGOHEADERS,
                                          'pays':pays})

#formulario de login
def login_view(request):
    #instancia de formulario
    form = loginForm()
    #validamos el metodo
    if request.method == "POST":
        user = authenticate(username=request.POST['user'],password=request.POST['password'])
        if user:
            login(request, user)
            return redirect("/admon/alumno/")
        else:
            return render(request,'login.html',{'context':'Login','error':'Usuario o contraseña incorrectos','form':form})#renderizar plantilla
    return render(request,'login.html',{'context':'Login','error':'','form':form})#renderizar plantilla

#pagina de logout
def logout_view(request):
    return render(request,'logout.html',{'context':'Logout'})