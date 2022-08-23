from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Student
from .flows import SchoolFlow
from .serializers import StudentSerializer
# Create your views here.


class StudentViewSet(ModelViewSet):
    serializer_class =  StudentSerializer
    queryset = Student.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        SchoolFlow.start.run(
            student = instance
        )
        return super().perform_create(serializer)