from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User

from .validators import username_exist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']


class UserMeSerializer(UserSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    def validate(self, data):
        instance = getattr(self, 'instance', None)
        if instance.role != User.ADMIN:
            data['role'] = instance.role
        return data


class UserSignUpSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email already exists!')
        return value

    def validate_username(self, value):
        if value == User.ME:
            raise serializers.ValidationError(
                'A user with this username already exists.'
            )
        return value


class UserAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[username_exist])
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code', 'token']

    def get_token(self, data):
        user = User.objects.get(username=data['username'])
        token = RefreshToken.for_user(user)
        return str(token.access_token)

    def validate(self, data):
        code = User.objects.get(username=data['username']).confirmation_code
        code_from_user = data.get('confirmation_code')
        if code_from_user is None:
            raise serializers.ValidationError(
                {'confirmation_code': 'This field is required.'}
            )

        if code != code_from_user:
            raise serializers.ValidationError(
                {'confirmation_code': 'Invalid value.'}
            )
        return data
