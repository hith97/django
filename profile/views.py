from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return Response(data)

class UpdateProfileView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
            
        user.save()
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }) 