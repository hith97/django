from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import DashboardOverviewSerializer, DashboardStatsSerializer

# Create your views here.

class DashboardOverviewAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DashboardOverviewSerializer

    def get(self, request, *args, **kwargs):
        # Add your dashboard overview logic here
        data = {
            'user': request.user.email,
            'total_items': 0,  # Replace with actual counts
            'recent_activities': [],  # Replace with actual activities
        }
        return Response(data)

class DashboardStatsAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DashboardStatsSerializer

    def get(self, request, *args, **kwargs):
        # Add your dashboard stats logic here
        data = {
            'stats': {
                'daily': {},
                'weekly': {},
                'monthly': {},
            }
        }
        return Response(data)
