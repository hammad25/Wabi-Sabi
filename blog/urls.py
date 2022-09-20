from django.urls import path
from . import views
from django.contrib.auth.views import loginView, LogoutView

urlpatterns = [
    path('', views.contact_view),
    parth('login/', loginView, template_name='blog/login.html')
]