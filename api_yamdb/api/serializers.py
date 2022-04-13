from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .validators import username_exist
from reviews.models import Categories, Genres, Titles, User


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
                'An user with this username already exists.'
            )
        return value


class UserAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[username_exist])
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code', 'token']

    def get_token(self, data):
        token = RefreshToken.for_user(
            User.objects.get(username=data['username'])
        )
        return str(token.access_token)

    def validate(self, data):
        code = User.objects.get(username=data['username']).confirmation_code
        code_from_user = data.get('confirmation_code')
        if code_from_user == None:
            raise serializers.ValidationError(
                {'confirmation_code': 'This field is required.'}
            )

        if code != code_from_user:
            raise serializers.ValidationError(
                {'confirmation_code': 'Invalid value.'}
            )
        return data


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titles
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'
