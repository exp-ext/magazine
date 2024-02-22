import random

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Comment, Rating


class CommentModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_owner = get_user_model().objects.create_user(email='testowner@test.com', password='testpassword12345owner')
        cls.user = get_user_model().objects.create_user(email='testuser@test.com', password='testpassword12345user')
        cls.test_object = cls.test_owner

        cls.comment = Comment.add_root_for_model(
            instance=cls.test_owner,
            user=cls.user,
            text='Тестовый комментарий',
        )
        cls.rating = Rating.create_for_model(
            user=cls.user,
            rating_value=random.randint(1, 10),
            instance=cls.comment,
        )

        for i in range(5):
            comment_l2 = cls.comment.add_child_for_model(
                text=f'This is a test comment-{i} level-2',
                user=cls.user,
            )
            Rating.create_for_model(
                instance=comment_l2,
                user=cls.user,
                rating_value=random.randint(1, 10)
            )
            for y in range(5):
                comment_l3 = comment_l2.add_child_for_model(
                    text=f'This is a test comment-{y} level-3',
                    user=cls.user,
                )
                Rating.create_for_model(
                    instance=comment_l3,
                    user=cls.user,
                    rating_value=random.randint(1, 10)
                )

    def test_comment_creation(self):
        """Тестирование создания комментария."""
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.text, 'Тестовый комментарий')
        self.assertEqual(self.comment.content_object, self.test_object)

    def test_get_comments_deeper_from_node(self):
        """Тестирование получения комментариев от узла."""

        comments_data = self.comment.get_comments_deeper_from_node()
        self.assertIn('text', comments_data[0])
        self.assertEqual(comments_data[0]['text'], 'Тестовый комментарий')
