from django.urls import path
from . import views
from .views import StaffAccountCreateView, StaffListView, StaffDeleteView, UserProfileView, EditProfileView
from .models import User

app_name = 'authentication'

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('create-admin/', views.CreateAdminUserAPIView.as_view(), name='create-admin'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('password/reset/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password/reset/verify/', views.PasswordResetVerifyOTPView.as_view(), name='password-reset-verify'),
    path('staff/create/', StaffAccountCreateView.as_view(), name='staff-create'),
    path('staff/', StaffListView.as_view(), name='staff-list'),
    path('staff/<int:id>/delete/', StaffDeleteView.as_view(), name='staff-delete'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),
] 

def get_queryset(self):
    return User.objects.filter(role__in=[User.Role.ORG_ADMIN, User.Role.REVIEWER]) 
