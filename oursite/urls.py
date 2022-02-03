from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('post_list/<str:slug>/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='create'),
    path('post/update/<int:post_id>/', PostUpdateView.as_view(), name='update'),
    path('post/delete/<int:post_id>/', PostDeleteView.as_view(), name='delete'),
    path('<slug:slug>/', post_detail, name='post_detail'),
]
