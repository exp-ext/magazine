from core.models import Create
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from ratings.models import Rating
from rest_framework.exceptions import ValidationError
from treebeard.mp_tree import MP_Node

from .serializers import CommentSerializer

User = get_user_model()


class Comment(MP_Node, Create):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name=_('автор комментария'))
    text = models.TextField(_('текст комментария'))

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    rating = GenericRelation(Rating, related_query_name='comments')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'{self.content_type} | {self.text}'

    @classmethod
    def add_root_for_model(cls, instance: models.Model, user: models.Model, text: str, **kwargs) -> models.Model:
        """
        Создает комментарий для указанного экземпляра модели.

        ### Args:
        - instance (`models.Model`): Экземпляр модели, к которой будет привязан комментарий.
        - user (`User`): Пользователь, оставляющий комментарий.
        - text (`str`): Текст комментария.
        - **kwargs: Дополнительные параметры.

        ### Returns:
        - `Comment`: Созданный объект комментария.
        """

        checks = {
            'instance': (instance, models.Model),
            'user': (user, get_user_model()),
        }

        for param_name, (param_value, expected_type) in checks.items():
            if not isinstance(param_value, expected_type):
                raise ValidationError(f'Переданный {param_name} не является экземпляром ожидаемой модели.')

        content_type = ContentType.objects.get_for_model(instance)
        comment = cls.add_root(
            user=user,
            text=text,
            content_type=content_type,
            object_id=instance.pk,
            **kwargs
        )
        return comment

    def add_child_for_model(self, user: models.Model, text: str, **kwargs) -> models.Model:
        """
        Создает дочерний комментарий для текущего комментария.

        ### Args:
        - user (`User`): Пользователь, оставляющий комментарий.
        - text (`str`): Текст комментария.
        - **kwargs: Дополнительные параметры.

        ### Returns:
        - `Comment`: Созданный объект комментария.
        """

        if not isinstance(user, get_user_model()):
            raise ValidationError('Переданный user не является экземпляром модели Django User.')

        comment = self.add_child(
            user=user,
            text=text,
            content_type=self.content_type,
            object_id=self.content_object.pk
        )
        return comment

    def __build_comment_tree(self, comments, parent=None):
        tree = []
        for comment in comments:
            if comment.get_parent() == parent:
                children = self.__build_comment_tree(comments, parent=comment)
                tree.append({
                    'comment': comment.children,
                    'children': children
                })
        return sorted(tree, key=lambda x: x['comment'].average_rating or 0, reverse=True)

    def get_comments_deeper_from_node(self):
        queryset = self.__class__.objects.filter(
            pk__in=self.get_descendants()
            .values_list('pk', flat=True) | self.__class__.objects.filter(pk=self.pk)
            .values_list('pk', flat=True)
        ).annotate(average_rating=Avg('rating__rating'))

        comments_list = list(queryset)
        comment_tree_data = self.__build_comment_tree(comments_list, parent=self)

        root_comment_data = {
            'comment': self,
            'children': comment_tree_data
        }
        return CommentSerializer(root_comment_data).data
