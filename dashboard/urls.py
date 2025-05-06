from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('overview/', views.DashboardOverviewAPIView.as_view(), name='overview'),
    path('stats/', views.DashboardStatsAPIView.as_view(), name='stats'),
    # Add more dashboard-related URLs as needed
] 