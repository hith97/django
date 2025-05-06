from rest_framework import generics, permissions
from rest_framework.response import Response
from authentication.models import User
from authentication.serializers import UserRegistrationSerializer, UserLoginSerializer

class RegisterAPI(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

class LoginAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role,
            }
        })
