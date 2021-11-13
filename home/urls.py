from  django.urls import  path

from .views import (
    index,
    categoryView
)

app_name = 'home'
urlpatterns = [
    path('', index, name='index'),
    path('category/<slug:slug>/', categoryView, name='category'),
]