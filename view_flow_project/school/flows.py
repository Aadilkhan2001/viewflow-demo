from viewflow.base import Flow,this
from viewflow import flow
from school.models import AdmissionProcess
from viewflow.flow.views import UpdateProcessView ,CreateProcessView
from viewflow.decorators import flow_start_func
from viewflow import frontend
import django_rq
from school.tasks import accepted, rejected


#starting process programattically  using startflow function 
#This function used in views.py to start a process on certain action
@flow_start_func
def start_flow(activation,**kwargs):
    activation.prepare()
    activation.process.student = kwargs.pop('student')
    activation.process.status_admission = kwargs.pop('status_admission',False)
    activation.done()
    return activation


#school flow is main flow of admission process 
@frontend.register
class SchoolFlow(Flow):

    process_class = AdmissionProcess

    #starting the flow
    start= (flow.StartFunction(
        start_flow ,
    ).Next(this.update_status))

    #first node is update status
    update_status = (
        flow.View(
            UpdateProcessView,
            fields=['status_admission']
        ).Permission(
            auto_create=True
        ).Next(this.check_status)
    )

    #check status is node that checks admission status after update by authority 
    #after that calling function accoridingly
    check_status =( flow.If(
            lambda activation : activation.process.status_admission
        ).Then(
            this.send
            
        ).Else(
            this.send_notapproved
        ))
    

    #calling a notify method 
    send =(
        flow.Handler(
            this.notify
        ).Next(
            this.end
        )
    )

    #calling notify_rejected method 
    send_notapproved = (flow.Handler(
        this.notify_rejected
    ).Next(this.end))

    #ending flow node
    end = flow.End()

    #view flow handler which adding a task into django rq queue
    def notify(self,activation):
        queue = django_rq.get_queue('student_notify')
        email = activation.process.student.email
        queue.enqueue(accepted,email=email)
    
    #view flow handler which adding a task into django rq queue
    def notify_rejected(self,activation):
        queue = django_rq.get_queue('student_notify')
        email = activation.process.student.email
        queue.enqueue(rejected,email=email)
