from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from .models import Plan, Cliente, Pago
from .forms import registerClient, loginForm, searchClient
from .enums import Headers, DatabaseColumns
from .forms import registerClient, loginForm, searchClient, searchClientByCurp, updateClientForm, registerPaymentForm
import datetime

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
                #validamos que exista el familiar
                Cliente.objects.filter(curp=request.POST["curp_familiar"]).update(id_plan=Plan.objects.get(id_plan="P-F"))
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
def updateAlumno(request):
    return render(request,'updateClient.html',{'context':'Modificar alumno'})

@login_required
def deleteAlumno(request):
    return render(request, 'deleteClient.html', {
        'context': 'Eliminar alumno',
        'error': '',
        'alumno': None
    })

@login_required
def buscar_alumno_eliminar(request):
    if request.method == "POST":
        curp = request.POST.get('curp_busqueda')
        try:
            alumno = Cliente.objects.get(curp=curp)
            return render(request, 'deleteClient.html', {
                'context': 'Eliminar alumno',
                'alumno': alumno,
                'error': ''
            })
        except Cliente.DoesNotExist:
            return render(request, 'deleteClient.html', {
                'context': 'Eliminar alumno',
                'alumno': None,
                'error': 'No se encontró ningún alumno con ese CURP'
            })
    return redirect('/admon/alumno/delet')

@login_required
def eliminar_alumno(request, curp):
    if request.method == "POST":
        try:
            alumno = Cliente.objects.get(curp=curp)
            alumno.delete()
            return redirect('/admon/alumno/')
        except Cliente.DoesNotExist:
            return render(request, 'deleteClient.html', {
                'context': 'Eliminar alumno',
                'alumno': None,
                'error': 'No se encontró ningún alumno con ese CURP'
            })
    return redirect('/admon/alumno/delet')
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

@login_required
def createPago(request):
    return render(request, 'pagoRegister.html', {
        'context': 'Registrar pago',
        'error': '',
        'alumno': None
    })

@login_required
def buscar_alumno_pago(request):
    if request.method == "POST":
        curp = request.POST.get('curp_busqueda')
        try:
            alumno = Cliente.objects.get(curp=curp)
            # Crear formulario con el monto predeterminado
            initial_data = {
                'monto': alumno.id_plan.mensualidad,
                'fecha_pago': datetime.date.today(),
                'tipo': 'Efectivo',
                'retrasado': False
            }
            form = registerPaymentForm(initial=initial_data)
            return render(request, 'pagoRegister.html', {
                'context': 'Registrar pago',
                'alumno': alumno,
                'form': form,
                'error': ''
            })
        except Cliente.DoesNotExist:
            return render(request, 'pagoRegister.html', {
                'context': 'Registrar pago',
                'alumno': None,
                'error': 'No se encontró ningún alumno con ese CURP'
            })
    return redirect('/admon/pago/register')

@login_required
def registrar_pago(request, curp):
    if request.method == "POST":
        try:
            alumno = Cliente.objects.get(curp=curp)
            # Registrar el pago
            Pago.objects.create(
                monto=request.POST['monto'],
                fecha_pago=request.POST['fecha_pago'],
                tipo=request.POST['tipo'],
                retrasado='retrasado' in request.POST,
                curp=alumno
            )
            return redirect('/admon/alumno/')
        except Exception as e:
            form = registerPaymentForm(request.POST)
            return render(request, 'pagoRegister.html', {
                'context': 'Registrar pago',
                'alumno': {'curp': curp},
                'form': form,
                'error': f'Error al registrar pago: {str(e)}'
            })
    return redirect('/admon/pago/register')

@login_required
def buscar_alumno(request):
    if request.method == "POST":
        curp = request.POST.get('curp_busqueda')
        try:
            alumno = Cliente.objects.get(curp=curp)
            # Crear formulario con datos del alumno
            initial_data = {
                'nombre': alumno.nombre,
                'direccion': alumno.direccion,
                'telefono': alumno.telefono,
                'correo': alumno.correo,
                'fecha_nac': alumno.fecha_nac,
                'es_plan_familiar': alumno.id_plan.id_plan == 'P-F',
            }
            
            # Si tiene plan familiar, buscar el CURP del familiar
            if alumno.id_plan.id_plan == 'P-F':
                # Aquí deberías implementar la lógica para encontrar el CURP del familiar
                # Por ahora lo dejamos vacío
                initial_data['curp_familiar'] = ''
                
            form = updateClientForm(initial=initial_data)
            return render(request, 'updateClient.html', {
                'context': 'Actualizar alumno',
                'alumno': alumno,
                'form': form,
                'error': ''
            })
        except Cliente.DoesNotExist:
            return render(request, 'updateClient.html', {
                'context': 'Actualizar alumno',
                'alumno': None,
                'error': 'No se encontró ningún alumno con ese CURP'
            })
    return redirect('/admon/alumno/update')
@login_required
def actualizar_alumno(request, curp):
    if request.method == "POST":
        try:
            alumno = Cliente.objects.get(curp=curp)
            # Actualizar datos del alumno
            alumno.nombre = request.POST['nombre']
            alumno.direccion = request.POST['direccion']
            alumno.telefono = request.POST['telefono']
            alumno.correo = request.POST['correo']
            alumno.fecha_nac = request.POST['fecha_nac']
            
            # Verificar si cambió el plan
            es_plan_familiar = 'es_plan_familiar' in request.POST
            if es_plan_familiar:
                alumno.id_plan = Plan.objects.get(id_plan="P-F")
                # Si hay CURP familiar, actualizar ese alumno también
                curp_familiar = request.POST.get('curp_familiar')
                if curp_familiar:
                    try:
                        familiar = Cliente.objects.get(curp=curp_familiar)
                        familiar.id_plan = Plan.objects.get(id_plan="P-F")
                        familiar.save()
                    except Cliente.DoesNotExist:
                        pass
            else:
                alumno.id_plan = Plan.objects.get(id_plan="P-R")
                
            alumno.save()
            return redirect('/admon/alumno/')
        except Exception as e:
            form = updateClientForm(request.POST)
            return render(request, 'updateClient.html', {
                'context': 'Actualizar alumno',
                'alumno': {'curp': curp},
                'form': form,
                'error': f'Error al actualizar: {str(e)}'
            })
    return redirect('/admon/alumno/update')