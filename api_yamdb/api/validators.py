from rest_framework import serializers

from reviews.models import User

USER_NOT_EXIST = "The user with this {username} doesn't exist."

def username_exists(username):
    if not User.objects.filter(username=username).exists():
        raise serializers.ValidationError(
            USER_NOT_EXIST
        )
