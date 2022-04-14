import uuid
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from .permissions import IsUserOrAdminOrModerOrReadOnly
from api_yamdb.settings import EMAIL_AUTH
from .serializers import (CategoriesSerializer, CommentSerializer, GenresSerializer,
                          ReviewSerializer, TitlesSerializer, UserAuthSerializer,
                          UserMeSerializer, UserSerializer,
                          UserSignUpSerializer)
from reviews.models import Categories, Comments, Genres, Review, Titles


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


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsUserOrAdminOrModerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Titles, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Titles, id=review_id)
        serializer.save(reviews=review, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsUserOrAdminOrModerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        comment = get_object_or_404(Comments, id=self.kwargs.get('comment_id'))
        return comment.all()

    def perform_create(self, serializer):
        comment_id = self.kwargs.get("comment_id")
        comment = get_object_or_404(Comments, id=comment_id)
        serializer.save(comments=comment, author=self.request.user)
