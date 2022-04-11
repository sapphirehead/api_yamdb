from django.contrib.auth.models import AbstractUser
from django.db import models


USERS_ROLES = ('user', 'moderator', 'admin')


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email',
        unique=True
    )
    username = models.CharField(
        verbose_name='username',
        max_length=30,
        unique=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=10,
        choices=USERS_ROLES,
        default='user'
    )
    biography = models.TextField(
        verbose_name='Биография',
        max_length=512,
        null=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=30,
        null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=40,
        null=True
    )

def __str__(self):
        return self.username