from django.contrib import admin
from .models import Student,AdmissionProcess


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["apply_date", "birth_date", "name"] [::-1]


@admin.register(AdmissionProcess)
class AdmissionProcessAdmin(admin.ModelAdmin):
    list_display = ["status_admission", "student"]
