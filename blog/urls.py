from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    # path('/accounts/login/', LoginView.as_view(name='blog/login.html')),
    # path('/accounts/logout/', LogoutView.as_view(name='blog/logout.html')),
    # path('contact/', views.contact_view ),
    # path('register/', views.register, name='register')
]