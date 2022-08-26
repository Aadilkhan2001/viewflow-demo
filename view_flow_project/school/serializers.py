from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id','name','birth_date','apply_date','email']
        read_only_fields = (['id','apply_date'])