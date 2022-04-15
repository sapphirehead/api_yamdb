from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
ME = 'me'
USER_CHOISES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin')
    ]

class User(AbstractUser):
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
            self.role = ADMIN
        elif self.role == ADMIN:
            self.is_staff = True
        else:
            self.is_staff = False

        super(User, self).save(*args, **kwargs)


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        related_name="titles",
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name="titles",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        'Оценка [ 1 .. 10 ] ',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text[:20]


class Comments(models.Model):
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.text[:20]
