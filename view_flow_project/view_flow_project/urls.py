from django.contrib import admin
from django.urls import path,include
from school.flows import SchoolFlow
from viewflow.flow.viewset import FlowViewSet
from school.views import StudentViewSet
from rest_framework.routers import DefaultRouter
from material.frontend import urls as frontend_urls
router = DefaultRouter()

router.register(r'',StudentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('school/',include(FlowViewSet(SchoolFlow).urls)),  
    path('',include(frontend_urls)),
    path('data/',include(router.urls))
]
    