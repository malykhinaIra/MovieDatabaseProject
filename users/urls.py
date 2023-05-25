from django.urls import path
from . import views


urlpatterns = [
    path('<str:username>/', views.UserProfileView.user_profile, name = 'user_profile'),
]


