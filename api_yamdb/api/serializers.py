from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import (ADMIN, ME, Categories, Comments, Genres, Review,
                            Titles, User)

from .validators import username_exists

CONFIRMATION_CODE_REQUIRED = {'confirmation_code': 'This field is required.'}
CONFIRMATION_CODE_INVALID = {'confirmation_code': 'Invalid value.'}
USERNAME_PROHIBITED = 'This username is prohibited. You should select other.'


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
        if instance.role != ADMIN:
            data['role'] = instance.role
        return data


class UserSignUpSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_username(self, value):
        if value == ME:
            raise serializers.ValidationError(USERNAME_PROHIBITED)
        return value


class UserAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[username_exists])
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
            raise serializers.ValidationError(CONFIRMATION_CODE_REQUIRED)
        elif code != code_from_user:
            raise serializers.ValidationError(CONFIRMATION_CODE_INVALID)
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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
