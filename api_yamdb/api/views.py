from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

User = get_user_model()

def get_user_token_auth():
    pass
def send_user_code():
    pass


class UserViewSet(viewsets.ModelViewSet):
    pass
