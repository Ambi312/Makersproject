from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('post_list/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='create'),
    path('post/update/<int:post_id>/', PostUpdateView.as_view(), name='update'),
    path('post/delete/<int:post_id>/', PostDeleteView.as_view(), name='delete'),
]
