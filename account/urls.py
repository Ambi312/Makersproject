from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import RegisterView, SingInView, profile, favourite_add, favourite_list

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', SingInView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile', profile, name='profile'),
    path('fav/<int:id>/', favourite_add, name='favourite_add'),
    path('profile/favourites/', favourite_list, name='favourite_list'),

]
