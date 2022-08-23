from django.db import models
from viewflow.models import Process

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    apply_date = models.DateTimeField(auto_now_add=True)



class AdmissionProcess(Process):
    student = models.OneToOneField(Student,on_delete=models.CASCADE)
    status_admission = models.BooleanField(default=False)

    def is_status(self):
        if self.status_admission == True:
            return True
        else:   
            return False
