from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('product-list/<str:slug>/', PostListView.as_view(), name='list'),
    path('product/<int:post_id>', PostDetailView.as_view(), name='detail'),
    path('product/create/', PostCreateView.as_view(), name='create'),
    path('product/update/<int:post_id>/', PostUpdateView.as_view(), name='update'),
    path('product/delete/<int:post_id>/', PostDeleteView.as_view(), name='delete'),
    path('search', SearchListView.as_view(), name='search'),
]
