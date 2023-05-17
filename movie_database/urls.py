"""movie_database URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from catalog import views as catalog_views
from main import views as main_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('', main_views.index, name='index'),
                  path('signup', user_views.signup, name='signup'),
                  path('search/', catalog_views.search, name='search'),
                  path('admin/', admin.site.urls),
                  path('user/', include('users.urls')),
                  path('movie/', include('catalog.urls')),
                  path('login', user_views.LoginUser, name='login_user'),
                  path('change_password', user_views.change_password, name='change_password'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
