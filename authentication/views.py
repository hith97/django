from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    PasswordResetRequestSerializer,
    PasswordResetVerifyOTPSerializer,
    AdminUserCreateSerializer,
    UserProfileSerializer
)
from .permissions import IsSuperAdmin, CanCreateAdminOrReviewer
from .models import User
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class LoginAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class RegisterAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

class CreateAdminUserAPIView(generics.CreateAPIView):
    permission_classes = (IsSuperAdmin, CanCreateAdminOrReviewer)
    serializer_class = AdminUserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': f'{user.get_role_display()} created successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role,
            }
        }, status=status.HTTP_201_CREATED)

class LogoutAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "OTP has been sent to your email."},
            status=status.HTTP_200_OK
        )

class PasswordResetVerifyOTPView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordResetVerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password has been reset successfully."},
            status=status.HTTP_200_OK
        )

class StaffAccountCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        # Check if the requesting user is a SUPERADMIN
        if not request.user.is_superadmin():
            return Response(
                {"detail": "Only SUPERADMIN can create staff accounts."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Validate the role
        role = request.data.get('role')
        if role not in [User.Role.ORG_ADMIN, User.Role.REVIEWER]:
            return Response(
                {"detail": "Invalid role. Must be either ORG_ADMIN or REVIEWER."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the user
        send_welcome = request.data.get('send_welcome_email', False)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if send_welcome:
            # Call your email sending function here
            send_mail(
                'Welcome to the Team!',
                'Hello and welcome to our platform!',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        return Response({
            "message": "Staff account created successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
            }
        }, status=status.HTTP_201_CREATED)
    
class StaffListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]  # Only admin can access
    serializer_class = UserRegistrationSerializer

    def get_queryset(self):
        # List all staff (ORG_ADMIN and REVIEWER)
        return User.objects.filter(role__in=[User.Role.ORG_ADMIN, User.Role.REVIEWER])
    

class StaffDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]  # Or customize as needed
    queryset = User.objects.all()
    lookup_field = 'id'  # or 'pk'


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
    

class EditProfileView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
