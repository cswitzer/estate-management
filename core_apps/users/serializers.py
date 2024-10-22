from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    """
    Override djosers UserCreateSerializer so that we can add our own custom fields
    to the user creation process
    """

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "username", "first_name", "last_name", "password")
