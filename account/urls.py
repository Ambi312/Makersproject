from django.contrib.auth.views import LogoutView
from django.urls import path

from oursite.views import favourite_add, favourite_list
from .views import RegisterView, SingInView, profile

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', SingInView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('login', profile, name='profile'),
    path('fav/<int:id>/', favourite_add, name='favourite_add'),
    path('fav/<int:id>/', favourite_list, name='favourite_list'),
]
