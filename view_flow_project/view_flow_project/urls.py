
from django.contrib import admin
from django.urls import path,include
from school.flows import SchoolFlow
from viewflow.flow.viewset import FlowViewSet
urlpatterns = [
    path('admin/', admin.site.urls),
    path('school/',include(FlowViewSet(SchoolFlow).urls))
]
