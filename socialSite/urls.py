from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:pk>/', views.post, name='post'),
    path('posts/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('posts/new_post/', views.make_post, name='new_post'),
    path('api/posts', views.posts_api, name='posts_api'),
    path('api/posts/<int:pk>', views.post_api, name='post_api'),
    path('xml/', views.xml_interface, name='xml_interface'),
]
