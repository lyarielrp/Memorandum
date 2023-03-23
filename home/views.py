from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import Empresa
# Create your views here.


def loguear(request):
    if request.user.is_authenticated:
                return redirect('Home')
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            usu=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usuario=authenticate(username=usu, password=pwd)
            if usuario is not None:
                login(request, usuario)
                return redirect('Home')
            else:
                messages.error(request, "Usuario no valido")
        else:
            messages.error(request, "Usuario no valido")
                
    form=AuthenticationForm()        
    return render(request,"registration/login.html",{"form":form})
    
class Login(LoginView):
    template_name="registration/login.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
                return redirect('Home')
        return super().dispatch(request, *args, **kwargs)

class Salir(RedirectView):
    template_name="registration/logged_out.html"
    pattern_name='login'
    
@login_required
def home(request):
    empresa = Empresa.objects.first()
    return render(request, "memorandum/base.html",{'empresa':empresa})
@login_required
def contacto(request):
    empresa = Empresa.objects.first()
    return render(request, "memorandum/contact.html",{'empresa':empresa})

