from django.shortcuts import render,redirect
from .models import Menorandum
from home.models import Empresa
from django.urls import reverse_lazy
from django.core.mail import send_mail,send_mass_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.html import strip_tags
from .forms import CrearMemorandumForm,ModificarMemorandumForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import UpdateView,DeleteView,DetailView

User=get_user_model()

# Create your views here.
@permission_required('memorandum.view_memorandum', login_url='loginn')
def memorandus(request):
    if request.user.is_authenticated:        
        memo = Menorandum.objects.filter(user=request.user)
        paginator = Paginator(memo, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'memo/list-memorandus.html',{'page_obj':page_obj})
        
    else:
        return redirect('login')
@permission_required('memorandum.add_memorandum', login_url='loginn')    
def add_memorandus(request):
    if request.method=='GET' and request.user.is_authenticated:
            return render(request, 'memo/add-memorandum.html', {'form': CrearMemorandumForm()},)
    
    
    if request.method=='POST' and request.user.is_authenticated :
        form = CrearMemorandumForm(request.POST, request.FILES)
        if form.is_valid():
            
            post=form.save(commit=False) 
            files=request.FILES.getlist('archivos')
            for f in files: 
                post.archivos=f
            post.email=request.user.email
            post.user=request.user
            post.save()
            
            """m=Menorandum.objects.create(
            nombre=request.POST['nombre'],
            texto=request.POST['texto'],
            email=request.user.email,
                                 
            date_expiring=request.POST['date_expiring'],
            user=request.user,       
            )            
            m.save()""" 
            
        
            return redirect('list_memorandums')
        else:
            return render(request, 'memo/add-memorandum.html', {
            'error': 'El formulario no es valido'
            },)
    
def invitar_lector(request,nombre):
    if request.method=='GET' and request.user.is_authenticated:
        empresa=Empresa.objects.first()
        user=User.objects.exclude(is_superuser=True,email=request.user.email).values('email')
       
        return render(request, 'emails/envio_emails.html', {'usuarios':user,'nombre':nombre,'empresa':empresa})
    else:
        return redirect('list_memorandums')

                    
def invitar(request):  
    if request.method=='POST' and request.user.is_authenticated :
        n=request.POST['nombre']
        id=Menorandum.objects.filter(user=request.user.id,nombre=n).values('id').first()
              
        enviar_mail(               
                nombre=request.POST['nombre'],
                para=request.POST['email'],
                email=request.user.email,
                slug=Menorandum.objects.filter(user=request.user.id,id=id["id"]).values('slug')
            )
        return redirect('list_memorandums')
    else:
        return redirect('home')
        
def enviar_mail(**kwargs):
    asunto="Haz sido invitado a leer el siguiente Memorandumn"
    mensaje=render_to_string("emails/email.html",{
        "nombre":kwargs.get("nombre"),
        "email":kwargs.get("email"),
        "ruta":kwargs.get("slug"),        
    })
    mensaje_texto=strip_tags(mensaje)
    from_email=settings.EMAIL_HOST_USER
    to=kwargs.get("para")
    
    send_mail(asunto,mensaje_texto,from_email,[to],html_message=mensaje)        
    
class UpdateMemo(UpdateView,LoginRequiredMixin,PermissionRequiredMixin):
    model = Menorandum
    form_class = ModificarMemorandumForm
    template_name = "memo/update_memo.html"
    success_url = reverse_lazy('list_memorandums') 
    permission_required = 'memorandum.change_memorandum'  
    
class DeleteMemo(DeleteView,LoginRequiredMixin,PermissionRequiredMixin):
    model = Menorandum
    template_name = "memo/delete_memo.html"
    success_url = reverse_lazy('list_memorandums')
    permission_required = 'memorandum.delete_memorandum'
    
class DetailMemo(DetailView,LoginRequiredMixin,PermissionRequiredMixin):
    model = Menorandum
    context_object_name='menorandum'
    template_name = "memo/menorandum_detail.html"
    
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['empresa']=Empresa.objects.first()
        #context['arch']=Menorandum.objects.filter(id=pk).values('archivos')
        return context
    
    
        
            
    
    
