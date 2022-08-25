from viewflow.base import Flow,this
from viewflow import flow
from school.models import AdmissionProcess
from viewflow.flow.views import UpdateProcessView ,CreateProcessView
from viewflow.decorators import flow_start_func
from viewflow import frontend
import django_rq
from school.tasks import accepted, rejected


@flow_start_func
def start_flow(activation,**kwargs):
    activation.prepare()
    activation.process.student = kwargs.pop('student')
    activation.process.status_admission = kwargs.pop('status_admission',False)
    activation.done()
    return activation

@frontend.register
class SchoolFlow(Flow):
    process_class = AdmissionProcess

    start= (flow.StartFunction(
        start_flow ,
    ).Next(this.update_status))


    update_status = (
        flow.View(
            UpdateProcessView,
            fields=['status_admission']
        ).Permission(
            auto_create=True
        ).Next(this.check_status)
    )

    check_status =( flow.If(
            lambda activation : activation.process.status_admission
        ).Then(
            this.send
            
        ).Else(
            this.send_notapproved
        ))
    

  

    send =(
        flow.Handler(
            this.notify
        ).Next(
            this.end
        )
    )

    send_notapproved = (flow.Handler(
        this.notify_rejected
    ).Next(this.end))

    end = flow.End()

    def notify(self,activation):
        queue = django_rq.get_queue('student_notify')
        queue.enqueue(accepted)
    
    def notify_rejected(self,activation):
        queue = django_rq.get_queue('student_notify')
        queue.enqueue(rejected)
