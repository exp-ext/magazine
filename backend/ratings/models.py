from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

User = get_user_model()


class Rating(models.Model):
    """
    Модель для хранения рейтингов пользователей.

    ### Field:
    - user (`ForeignKey[User]`): Пользователь, оставивший рейтинг.
    - rating (`BigIntegerField`): Рейтинг.
    - content_type (`ForeignKey[ContentType]`): Модель контента, к которому привязан рейтинг.
    - object_id (`PositiveIntegerField`): Идентификатор объекта.
    - content_object (`GenericForeignKey`): Обобщенный внешний ключ для связи с контентом.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', verbose_name=_('автор комментария'))
    rating = models.BigIntegerField(
        _('рейтинг'),
        default=5,
        editable=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'рейтинг'
        verbose_name_plural = 'рейтинги'
        ordering = ('-rating',)

    def __str__(self):
        return f'{self.content_type} | {self.rating}'

    @classmethod
    def create_for_model(cls, instance: models.Model, user: models.Model, rating_value: int = 0, **kwargs) -> models.Model:
        """
        Создает объект рейтинга для указанного экземпляра модели.

        ### Args:
        - instance (`models.Model`): Экземпляр модели к которой будет привязан Rating.
        - user (`models.Model`): Пользователь, оставляющий рейтинг.
        - rating_value (`int`, опционально): Значение рейтинга (по умолчанию 0).
        - **kwargs: Дополнительные параметры.

        ### Returns:
        - `Rating`: Созданный объект рейтинга.

        """
        checks = {
            'instance': (instance, models.Model),
            'user': (user, get_user_model()),
        }

        for param_name, (param_value, expected_type) in checks.items():
            if not isinstance(param_value, expected_type):
                raise ValidationError(f'Переданный {param_name} не является экземпляром ожидаемой модели.')

        content_type = ContentType.objects.get_for_model(instance)
        rating = cls.objects.create(
            user=user,
            rating=rating_value,
            content_type=content_type,
            object_id=instance.pk,
            **kwargs
        )
        return rating
