from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('me/', views.UserProfileView.as_view(), name='user-profile'),
    path('update/', views.UpdateProfileView.as_view(), name='update-profile'),
] 