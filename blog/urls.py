from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.PostList.as_view(), name='articles'),
    path('article/<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('favourite/<slug:slug>', views.favourite_post, name='post_favourite'),
    path('update/<slug:pk>', views.update_comment, name='update_comment'),
    path('delete/<slug:pk>', views.delete_comment, name='delete_comment'),
    path('contact', views.contact_view, name='contact'),
    path('contact/add', views.contact_add, name='contactadd'),
    path('about', views.about_view, name='about'),
    path('account/signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
]

urlpatterns += staticfiles_urlpatterns()