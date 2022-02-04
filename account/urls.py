from django.contrib.auth.views import LogoutView
from django.urls import path

from oursite.views import favourite_add, favourite_list
from .views import RegisterView, SingInView, profile

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', SingInView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile', profile, name='profile'),
]
