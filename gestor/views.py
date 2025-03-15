from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("<h1>Gestor AVAG</h1>")

def createAlumno(request):
    return HttpResponse("<h1>Nuevo alumno</h1>")

def updateAulmno(request):
    return HttpResponse("<h1>Cambiar datos de alumno</h1>")

def deleteAlumno(request):
    return HttpResponse("<h1>Eliminar alumno</h1>")