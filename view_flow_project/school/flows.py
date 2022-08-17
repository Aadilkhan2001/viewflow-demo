from viewflow.base import Flow,this
from viewflow import flow
from .models import AdmissionProcess
from viewflow.flow.views import UpdateProcessView ,CreateProcessView


class SchoolFlow(Flow):
    process_class = AdmissionProcess

    start= (flow.Start(
        CreateProcessView ,
        fields = ['status']
    ).Permission(
        auto_create=True
    ).Next(this.check_status))

    check_status = (    
        flow.Handler(
            flow.If(
            lambda activation : activation.process.is_status() == False
        ).Then(
            this.update_status
        ).Else(
            this.notify
        )
        )
    )

    update_status = (
        flow.View(
            UpdateProcessView,
            fields=['status']
        ).Permission(
            auto_create=True
        ).Next(this.end)
    )

    end = flow.End()

    def notify(activation):
        print("Admission accepted!!")