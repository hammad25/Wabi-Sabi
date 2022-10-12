from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('articles', views.PostList.as_view(), name='articles'),
    path('article/<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('delete_comment_confirm', views.delete_comment_confirm, name='delete_comment_confirm'),
    path('contact', views.contact_view, name='contact'),
    path('contact/add', views.contact_add, name='contactadd'),
    path('about', views.about_view, name='about'),
    path('account/signup', views.signup, name='signip'),
    path('profile', views.profile, name='profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),

    # path('/accounts/login/', LoginView.as_view(name='blog/login.html')),
    # path('/accounts/logout/', LogoutView.as_view(name='blog/logout.html')),
    # path('register/', views.register, name='register')
]

urlpatterns += staticfiles_urlpatterns()