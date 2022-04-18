from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import (
    ADMIN, ME, Category, Comment, Genre, Review, Title, User
)

from .validators import username_exists

CONFIRMATION_CODE_REQUIRED = {'confirmation_code': 'This field is required.'}
CONFIRMATION_CODE_INVALID = {'confirmation_code': 'This is an invalid value.'}
USERNAME_PROHIBITED = (
    'The {username} is prohibited.',
    'You should select another.'
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']


class UserMeSerializer(UserSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    def validate(self, data):
        instance = getattr(self, 'instance')
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
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, review):
        if self.context['request'].method != 'POST':
            return review

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'You have already written a review for this work.'
            )
        return review

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
