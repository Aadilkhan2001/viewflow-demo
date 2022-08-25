from django_rq import job

@job
def accepted():
    print("ACcepted")

@job
def rejected():
    print("Rejected")