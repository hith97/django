from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from .models import PasswordResetOTP, User

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Try to find user by email first
        try:
            user = User.objects.get(email=attrs['email'])
            # Try to authenticate with username
            auth_user = authenticate(username=user.username, password=attrs['password'])
            if not auth_user:
                raise serializers.ValidationError('Invalid credentials')
            if not auth_user.is_active:
                raise serializers.ValidationError('User account is disabled')
            return auth_user
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number'),
            role=validated_data.get('role', User.Role.USER)
        )
        return user

class AdminUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[User.Role.ORG_ADMIN, User.Role.REVIEWER])

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password', 'first_name', 'last_name', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")

    def save(self):
        user = self.user
        # Generate OTP
        otp = PasswordResetOTP.generate_otp()
        PasswordResetOTP.objects.create(user=user, otp=otp)

        # Send email with OTP
        send_mail(
            'Password Reset OTP',
            f'Your OTP for password reset is: {otp}\nThis OTP is valid for 10 minutes.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return user

class PasswordResetVerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Validate passwords match
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        # Validate password strength
        try:
            validate_password(attrs['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        # Validate OTP
        try:
            user = User.objects.get(email=attrs['email'])
            otp_obj = PasswordResetOTP.objects.filter(
                user=user,
                otp=attrs['otp'],
                is_used=False
            ).latest('created_at')

            if not otp_obj.is_valid():
                raise serializers.ValidationError({"otp": "OTP has expired"})

            self.otp_obj = otp_obj
            self.user = user
            return attrs

        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            raise serializers.ValidationError({"otp": "Invalid OTP"})

    def save(self):
        # Set new password
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()
        
        # Mark OTP as used
        self.otp_obj.is_used = True
        self.otp_obj.save()
        
        return self.user 
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role']
        read_only_fields = ['id', 'email', 'role']  # Email/role usually not editable, but you can adjust
