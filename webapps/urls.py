"""
URL configuration for webapps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
import maps.views as map_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # webapp pages:
    path('', map_views.home, name="home"),
    path('floor/<int:floor_id>', map_views.floor, name="floor"),
    path('profile', map_views.profile, name="profile"),

    # authentication:
    # have log in and logout handled by the default django things... 
    path('login', auth_views.LoginView.as_view(template_name="maps/login.html"), name="login"), 
    path('logout', map_views.logout_user, name="logout"),

    path('sign-up', map_views.sign_up, name="sign-up"),
    path('password-reset', map_views.home, name="password_reset"),

    # endpoints: 
    path('get_maps_script', map_views.get_maps_script),
    path('get_map_pins', map_views.get_map_pins),

    path('update_navigation_directions', map_views.update_navigation_directions, name="update-navigation"),
    # remove these two endpoints
    path('update_user_location', map_views.update_user_location), 
    path('get_user_location', map_views.get_user_location),
    
]
