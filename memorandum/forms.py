from django import forms
from django.forms import ModelForm,DateField
from .models import Menorandum

class DateInput(forms.DateInput):
    input_type='date'
    
class CrearMemorandumForm(ModelForm):    
    class Meta:
        model=Menorandum
        fields = ['nombre','texto','archivos','date_expiring']
        exclude = ['email','slug','user','created_at']
        widgets = {
            'date_expiring': DateInput(),
            'archivos': forms.ClearableFileInput(attrs={'multiple': True}),
        }
        
        
class ModificarMemorandumForm(ModelForm):
    class Meta:
        model=Menorandum
        fields = ['nombre','texto','archivos','date_expiring']
        exclude = ['email','slug','user','created_at']
        widgets = {
            'date_expiring': DateInput(),
            'archivos': forms.ClearableFileInput(attrs={'multiple': True}),
        }
        

    