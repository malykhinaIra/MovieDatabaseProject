from django.urls import path
from . import views


urlpatterns = [
    path('<str:username>/', views.user, name = 'user'),
    path('<str:username>/favourites/', views.favourites, name='favourites'),
]


