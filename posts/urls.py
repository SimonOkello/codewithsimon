from  django.urls import  path

from . import views
app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:post_id>/', views.postDetail, name='post-detail'),
    path('create/', views.createPost, name='create-post'),
    path('<str:post_id>/edit/', views.editPost, name='edit-post'),
    path('<str:post_id>/delete/', views.deletePost, name='delete-post'),
]