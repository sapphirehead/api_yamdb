import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api_yamdb.settings import EMAIL_AUTH

from .serializers import (UserAuthSerializer, 
                            UserMeSerializer, 
                            UserSerializer,
                          UserSignUpSerializer)

User = get_user_model()

@api_view(['POST'])
def signup_user(request):
    serializer = UserSignUpSerializer(data=request.data, many=False)
    serializer.is_valid(raise_exception=True)
    confirmation_code = uuid.uuid4()
    serializer.save(confirmation_code=confirmation_code)

    email = serializer.validated_data['email']
    send_mail(
        'You should use the next',
        f'confirmation_code: {confirmation_code}',
        EMAIL_AUTH,
        [email],
        fail_silently=False,
    )
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_auth_token(request):
    serializer = UserAuthSerializer(data=request.data, many=False)
    if serializer.is_valid():
        token = serializer.data['token']
        return Response({'token': token}, status=status.HTTP_200_OK)

    username_error = serializer.errors.get('username')
    if username_error is not None:
        for error in username_error:
            if error.code == 'invalid':
                return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAdminUser,)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated])
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
