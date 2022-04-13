import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api_yamdb.settings import EMAIL_AUTH
from .serializers import (CategoriesSerializer, GenresSerializer,
                          TitlesSerializer, UserAuthSerializer,
                          UserMeSerializer, UserSerializer,
                          UserSignUpSerializer)
from reviews.models import Categories, Genres, Titles

User = get_user_model()


@api_view(['POST'])
def signup_user(request):
    serializer = UserSignUpSerializer(data=request.data, many=False)
    serializer.is_valid(raise_exception=True)
    confirmation_code = uuid.uuid4()
    serializer.save(confirmation_code=confirmation_code)
    email = serializer.validated_data['email']
    send_mail(
        'YaMDB: Confirmation code for account',
        f'You should use the next confirmation_code: {confirmation_code}',
        EMAIL_AUTH,
        [email],
        fail_silently=False,
    )
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_auth_token(request):
    serializer = UserAuthSerializer(data=request.data, many=False)
    if serializer.is_valid():
        return Response(
            {'token': serializer.data['token']}, status=status.HTTP_200_OK
        )
    elif serializer.errors.get('username') != None:
        for error in serializer.errors.get('username'):
            if error.code == 'invalid':
                return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAdminUser,)
    lookup_field = 'username'

    @action(
        detail=False, 
        methods=['GET', 'PATCH'], 
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = UserMeSerializer(user, data=request.data, many=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
