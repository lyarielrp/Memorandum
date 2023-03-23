from django.conf import settings
from django.db import models
from djrichtextfield.models import RichTextField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import pre_save,post_save
from django.contrib.auth import get_user_model
from datetime import date 
from django.contrib.sites.models import Site


User=get_user_model()
def user_directory_path(instance, filename):
    return "user_{0}/{1}/{2}".format(instance.user.username, instance.nombre, filename)

class Menorandum(models.Model):
    nombre=models.CharField(verbose_name='Titulo',max_length=200)
    texto=RichTextField()
    email=models.EmailField(verbose_name='Correo Electronico',max_length=255)
    archivos=models.FileField(upload_to=user_directory_path, null=True, blank=True)
    date_expiring=models.DateField(verbose_name='Fecha de Expiracion', null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    slug=models.SlugField(max_length=200, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def save(self,*args, **kwargs):
        m=Menorandum.objects.filter(date_expiring__lte=date.today())
        m.delete()        
        return super(Menorandum, self).save( *args, **kwargs)
    
    class Meta:
        verbose_name="Memorandum"
        verbose_name_plural="Memorandums"
        permissions=(('can_download_file','Puede descargar archivos asociados'),)

    REQUIRED_FIELDS=['nombre','texto','email']
    
    def __str__(self):
        return self.nombre
def slug_generator(sender,instance,**kwargs):
    if not instance.slug:
        
        instance.slug = Site.objects.get_current().domain + '/memos/detail_memo/' + str(instance.user.username) + '/' + str(instance.id)
        
post_save.connect(slug_generator, sender = Menorandum)