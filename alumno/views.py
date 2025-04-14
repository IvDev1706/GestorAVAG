from django.shortcuts import render
from .forms import LoginForm
from gestor.enums import DatabaseColumns

# Create your views here.
def login_view(request):
    if request.method == "GET":
        return render(request, 'loginAlu.html', {'context':'Login',
                                          'error':'',
                                          'form':LoginForm()})
    else:
        print(request.POST[DatabaseColumns.ALUMNOCOLUMNS[0]])
        return render(request, 'loginAlu.html', {'context':'Login',
                                          'error':'',
                                          'form':LoginForm()})