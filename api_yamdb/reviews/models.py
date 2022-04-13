from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ME = 'me'
    USER_CHOISES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]
    username = models.CharField('username', max_length=32, unique=True)
    email = models.EmailField('email', max_length=64, unique=True)
    first_name = models.CharField(
        'Имя',
        max_length=32,
        blank=True,
        unique=False
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
        unique=False
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=USER_CHOISES,
        default=USER
    )
    confirmation_code = models.TextField(
        'Код подтверждения',
        null=True,
        blank=True
    )
    exclude = ('confirmation_code',)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ADMIN
        elif self.role == self.ADMIN:
            self.is_staff = True
        else:
            self.is_staff = False

        super(User, self).save(*args, **kwargs)
