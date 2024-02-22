from core.models import Create
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Avg, QuerySet
from django.utils.translation import gettext_lazy as _
from ratings.models import Rating
from rest_framework.exceptions import ValidationError
from treebeard.mp_tree import MP_Node

from .serializers import CommentTreeSerializer

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

    def __preprocess_comments(self, queryset: QuerySet):
        """
        Предварительная обработка комментариев для построения карты дочерних комментариев.

        ### Args:
        - queryset: Запрос к комментариям.

        ### Returns:
        - `dict`: Карта дочерних комментариев.

        """
        children_map = {}
        for comment in queryset:
            parent = comment.get_parent()
            parent_id = parent.id if parent else None
            if parent_id not in children_map:
                children_map[parent_id] = []
            children_map[parent_id].append(comment)
        return children_map

    def __build_comment_tree(self, children_map: dict, parent_id: int = None):
        """
        Построение дерева комментариев на основе карты дочерних комментариев.

        ### Args:
        - children_map (`dict`): Карта дочерних комментариев.
        - parent_id (`int`, опционально): Идентификатор родительского комментария.

        ### Returns:
        - `list`: Дерево комментариев.

        """
        children = children_map.get(parent_id, [])
        sorted_children = sorted(children, key=lambda x: x.average_rating or 0, reverse=True)
        tree = []
        for child in sorted_children:
            child_data = CommentTreeSerializer(child).data
            child_data['children'] = self.__build_comment_tree(children_map, child.id)
            tree.append(child_data)
        return tree

    def get_comments_deeper_from_node(self):
        """
        Получение дочерних комментариев из указанного узла в дереве, включая сам узел.

        ### Returns:
        - `list`: Дерево комментариев.

        """
        queryset = self.__class__.objects.filter(
            pk__in=self.get_descendants()
            .values_list('pk', flat=True) | self.__class__.objects.filter(pk=self.pk)
            .values_list('pk', flat=True)
        ).annotate(average_rating=Avg('rating__rating')).select_related('user')

        comments_list = list(queryset)
        children_map = self.__preprocess_comments(comments_list)
        comment_tree = self.__build_comment_tree(children_map)
        return comment_tree

    # def __build_comment_tree(self, comments, parent=None):
    #     tree = []
    #     for comment in comments:
    #         if comment.get_parent() == parent:
    #             serializer = CommentTreeSerializer(comment).data
    #             serializer.update({
    #                 'children': self.__build_comment_tree(comments, parent=comment)
    #             })
    #             tree.append(serializer)
    #     return sorted(tree, key=lambda x: x['average_rating'] or 0, reverse=True)

    # def get_comments_deeper_from_node(self):
    #     queryset = self.__class__.objects.filter(
    #         pk__in=self.get_descendants()
    #         .values_list('pk', flat=True) | self.__class__.objects.filter(pk=self.pk)
    #         .values_list('pk', flat=True)
    #     ).annotate(average_rating=Avg('rating__rating')).select_related('user')

    #     comments_list = list(queryset)
    #     return self.__build_comment_tree(comments_list)
