from django.shortcuts import render, redirect
from .forms import LoginForm
from gestor.models import Cliente, Pago
from gestor.enums import DatabaseColumns, Headers

# Create your views here.
def login_view(request):
    error = ""
    
    #la ruta en post
    if request.method == "POST":
        #instancia de formulario
        form = LoginForm(request.POST)
        #validacion del forumario
        if form.is_valid():
            #obtener el curp ingresado
            curp = form.cleaned_data['curp']
            #verificamos que exista en la bd
            try:
                cliente = Cliente.objects.get(curp=curp)
                #guardamos el id en la request
                request.session['cliente_curp'] = cliente.curp
                return redirect('/alumno/miinfo/')
            except Cliente.DoesNotExist:
                error = "El alumno no existe o la curp esta mal escrita"
    else:
        form = LoginForm()
    
    #ruta get
    return render(request, 'loginAlu.html', {'context':'Login',
                                          'error':error,
                                          'form':form})

#ruta principal del alumno
def cliente_index(request):
    #proteccion de ruta
    curp = request.session.get('cliente_curp')
    
    if not curp:
        return redirect('/')#redireccion al login
    
    #vista del index
    return render(request, 'indexAlu.html', {'context':'Mi informacion',
                                             'cliente':Cliente.objects.get(curp=curp)
                                             })
#ruta de historial de pagos
def cliente_history(request):
    #proteccion de ruta
    curp = request.session.get('cliente_curp')
    
    if not curp:
        return redirect('/')#redireccion al login
    
    #obtencion de los pagos (no mas de 12 meses atras)
    all_pays = Pago.objects.all().order_by(DatabaseColumns.PAGOCOLUMNS[2])[:12]
    
    return render(request,'historyAlu.html',{"context":"Historial de pagos",
                                             "headers":Headers.PAGOHEADERS,
                                             "pays":all_pays})

#ruta de cierre de sesion
def logout_view(request):
    #eliminar la curp guardada
    request.session.flush()
    
    return render(request, 'logoutAlu.html', {'context':'Logout'})  