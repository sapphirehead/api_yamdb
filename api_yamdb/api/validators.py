from rest_framework import serializers

from reviews.models import User


def username_exists(username):
    if not User.objects.filter(username=username).exists():
        raise serializers.ValidationError(
            "The user with this username doesn't exist."
        )
