"""
URL configuration for lhs_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.http import JsonResponse

def home_view(request):
    return JsonResponse({"message": "Welcome to the API! Use /api/v1/auth/ for authentication endpoints"})

# API URL patterns
api_patterns = [
    path('auth/', include('authentication.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('profile/', include('user_profile.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_patterns)),  # Version 1 of your API
    path('', home_view, name='home'),
]
