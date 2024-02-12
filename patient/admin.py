from django.contrib import admin
from .models import Patient
from . import models
# Register your models here.
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name','mobile_no']

    def first_name(self, obj):
        return obj.user.first_name

admin.site.register(Patient, PatientAdmin)