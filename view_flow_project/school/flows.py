from viewflow.base import Flow,this
from viewflow import flow
from .models import AdmissionProcess
from viewflow.flow.views import UpdateProcessView ,CreateProcessView
from viewflow.decorators import flow_start_func
from viewflow import admin


@flow_start_func
def start_flow(activation,**kwargs):
    activation.prepare()
    activation.process.student = kwargs.pop('student')
    activation.process.status_admission = kwargs.pop('status_admission',False)
    activation.done()
    return activation

class SchoolFlow(Flow):
    process_class = AdmissionProcess

    start= (flow.StartFunction(
        start_flow ,
    ).Next(this.check_status))

    check_status =( flow.If(
            lambda activation : activation.process.status_admission
        ).Then(
            this.send
            
        ).Else(
            this.update_status
        ))
    

    update_status = (
        flow.View(
            UpdateProcessView,
            fields=['status_admission']
        ).Permission(
            auto_create=True
        ).Next(this.send)
    )

    send =(
        flow.Handler(
            this.notify
        ).Next(
            this.end
        )

    )

    end = flow.End()

    def notify(self,activation):
        print("Admission accepted!!")