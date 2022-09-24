from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('articles', views.PostList.as_view(), name='articles'),
    path('contact', views.contact_view, name='contact'),
    path('contact/add', views.contact_add, name='contactadd'),
    path('about', views.about_view, name='about'),
    path('account/signup', views.signup, name='signip'),

    # path('/accounts/login/', LoginView.as_view(name='blog/login.html')),
    # path('/accounts/logout/', LogoutView.as_view(name='blog/logout.html')),
    # path('register/', views.register, name='register')
]