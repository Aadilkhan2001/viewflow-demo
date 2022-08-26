from django.db import models
from viewflow.models import Process

# student model 
class Student(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    apply_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(default='demo@gmail.com')


#process model which is contain process instance of admission flow
class AdmissionProcess(Process):
    student = models.OneToOneField(Student,on_delete=models.CASCADE)
    status_admission = models.BooleanField(default=False)

    def is_status(self):
        if self.status_admission == True:
            return True
        else:   
            return False
