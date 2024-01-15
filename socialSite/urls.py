from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:pk>/', views.post, name='post'),
    path('posts/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('posts/new_post/', views.make_post, name='new_post')
]
