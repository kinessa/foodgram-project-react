from djoser.serializers import UserCreateSerializer

from .models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = (
            'id', 'email', 'username', 'password', 'first_name', 'last_name'
        )
