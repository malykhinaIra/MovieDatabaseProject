from django.urls import path
from . import views


urlpatterns = [
    path('<str:username>/', views.user, name='users'),
    path('<str:username>/favourites/', views.favourites, name='favourites'),
]