from django_rq import job
from django.core.mail import send_mail
from django.conf import settings



#sending mail to student about his admission status approved by authority using django rq job
@job
def accepted(**kwargs):
    sender = settings.EMAIL_HOST_USER
    reciever  = kwargs.pop('email')
    body = """Hi congratulation !!
            Your admission is approved by authorities."""
    subject = "Regarding Admission!!"
    send_mail(subject=subject,message=body,from_email=sender,recipient_list=[reciever])
    
#sending mail to student about his admission status rejected by authority using django rq job
@job
def rejected(**kwargs):
    sender = settings.EMAIL_HOST_USER
    reciever  = kwargs.pop('email')
    body = """Sorry 
            Your admission is rejected by authorities.
            Better Luck Next time!!"""
    subject = "Regarding Admission!!"
    send_mail(subject=subject,message=body,from_email=sender,recipient_list=[reciever])