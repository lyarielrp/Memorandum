from django.contrib import admin
from .models import Menorandum
from solo.admin import SingletonModelAdmin
# Register your models here.
admin.site.register(Menorandum)
