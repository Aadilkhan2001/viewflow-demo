from django.contrib import admin
from .models import Student,AdmissionProcess
from viewflow.admin import ProcessAdmin

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["apply_date", "birth_date", "name"] [::-1]

admin.site.register(AdmissionProcess, ProcessAdmin)