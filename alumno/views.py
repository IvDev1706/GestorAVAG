from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from datetime import datetime
from decimal import Decimal
import json
import stripe
import stripe.error
from .forms import LoginForm
from gestor.models import Cliente, Pago
from gestor.enums import DatabaseColumns, Headers

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def login_view(request):
    #proteccion de ruta
    curp = request.session.get('cliente_curp')
    
    #caso de que no se cierra la sesion como es debido
    if curp:
        request.session.flush()#eliminar session abierta
    
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
                                             'cliente':Cliente.objects.get(curp=curp),
                                             'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
                                             })
#ruta de historial de pagos
def cliente_history(request):
    #proteccion de ruta
    curp = request.session.get('cliente_curp')
    
    if not curp:
        return redirect('/')#redireccion al login
    
    #obtencion de los pagos (no mas de 12 meses atras)
    all_pays = Pago.objects.filter(curp_id=request.session.get('cliente_curp')).order_by(DatabaseColumns.PAGOCOLUMNS[2])[:12]
    
    return render(request,'historyAlu.html',{"context":"Historial de pagos",
                                             "headers":Headers.PAGOHEADERS,
                                             "pays":all_pays,
                                             'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})

#ruta de pago de membresia
def cliente_payment(request):
    #proteccion de ruta
    curp = request.session.get('cliente_curp')
    
    if not curp:
        return redirect('/')
    
    cliente = Cliente.objects.get(curp=curp)
    
    #validacion de atraso
    fechaA = datetime.now()
    fechaT = datetime(fechaA.year, fechaA.month, 5)
    monto =  (cliente.id_plan.mensualidad + Decimal("50.0")) if fechaA > fechaT else cliente.id_plan.mensualidad#la fecha pasa del 5 del mes
    
    #renderizamos la pagina
    return render(request,'paymentView.html',{"context":"Pago de membresia",
                                              "cliente":cliente,
                                              "monto":monto,
                                              "fecha":fechaA.strftime("%Y-%m-%d"),
                                              'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
                                              })

#ruta de checkout session
@csrf_exempt
def checkout_session(request, *args, **kwargs):
    if request.method == "POST":
        cliente = Cliente.objects.get(curp=request.session.get('cliente_curp'))
        #obtener los datos mandados desde front
        data = json.loads(request.body)
        amount_pesos = float(data.get("amount", 0))
        amount_centavos = int(amount_pesos * 100)  # Stripe usa centavos
        
        #creamos la secion
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],#metodo de pago
            line_items=[{
                'price_data':{
                    'currency':'mxn',
                    "product_data":{
                        'name':'Pago de membresia mensual',
                    },
                    'unit_amount':amount_centavos,#cantidad en centavos
                },
                'quantity':1
            }],
            metadata={
                "cliente_id":cliente.curp
            },
            mode='payment',
            success_url="http://localhost:8000/alumno/payment/success",
            cancel_url="http://localhost:8000/alumno/payment/abort"
        )
        
        return JsonResponse({'id':session.id})
    
#ruta de webhook para registrar pagos
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    
    #creacion d evento
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVErificationError as e:
        return HttpResponse(status=400)
    
    #captura del evento
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        fechaA = datetime.now()
        fechaT = datetime(fechaA.year, fechaA.month, 5)
        retrasado = True if fechaA > fechaT else False
        cliente = Cliente.objects.get(curp=session['metadata'].get('cliente_id'))
        monto = (cliente.id_plan.mensualidad + Decimal("50.0")) if retrasado else cliente.id_plan.mensualidad
        
        #crear el objeto pago
        Pago.objects.create(monto=monto, fecha_pago=fechaA, tipo="Tarjeta", retrasado=retrasado, curp = cliente)
        
    
    return HttpResponse(status=200)
def succes_pay(request):
    #proteccion de ruta
    curp = request.session.get('cliente_curp')
    
    if not curp:
        return redirect('/')
    
    return render(request,'successPayView.html',{'content':'Pago exitoso'})

def aborted_pay(request):
    #proteccion de ruta
    curp = request.session.get('cliente_curp')
    
    if not curp:
        return redirect('/')
    
    return render(request,'abortedPayView.html',{'content':'Pago no realizado'})

#ruta de cierre de sesion
def logout_view(request):
    #eliminar la curp guardada
    request.session.flush()
    
    return render(request, 'logoutAlu.html', {'context':'Logout'})  