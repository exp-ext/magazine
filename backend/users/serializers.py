from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (CharField, ModelSerializer, Serializer,
                                        ValidationError)

User = get_user_model()


class UserSerializer(ModelSerializer):
    """
    Сериализатор для работы с моделью User.
    """
    first_name = CharField(max_length=150, required=True)
    last_name = CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'first_name',
            'last_name',
            'password',
        )


class SetPasswordSerializer(Serializer):
    """Изменение пароля текущего пользователя."""
    new_password = CharField()
    current_password = CharField()

    class Meta:
        model = User
        fields = (
            'new_password',
            'current_password',
        )
        extra_kwargs = {
            'new_password': {'required': True, 'allow_blank': False},
            'current_password': {'required': True, 'allow_blank': False},
        }

    def validate(self, obj):
        validate_password(obj['new_password'])
        return super().validate(obj)

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['current_password']):
            raise ValidationError({'current_password': 'Неправильный пароль.'})

        if validated_data['current_password'] == validated_data['new_password']:
            raise ValidationError({'new_password': 'Новый пароль должен отличаться от текущего.'})

        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data
