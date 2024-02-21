from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """
    Менеджер пользователей для настройки создания пользователей.
    """
    def create_user(self, email: str, password: str, first_name: str = None, last_name: str = None, is_staff: bool = False, is_superuser: bool = False, is_verified: bool = False):
        """
        Создает и сохраняет пользователя с указанными данными.

        ### Args:
        - email (`str`): Email пользователя.
        - password (`str`): Пароль пользователя.
        - first_name (`str`, опционально): Имя пользователя.
        - last_name (`str`, опционально): Фамилия пользователя.
        - is_staff (`bool`, опционально): Установлен ли пользователь в состояние персонала.
        - is_superuser (`bool`, опционально): Установлен ли пользователь в состояние суперпользователя.
        - is_verified (`bool`, опционально): Подтвержден ли пользователь.

        ### Raises:
        - ValueError: Если email или пароль отсутствуют.

        ### Returns:
        - `User`: Созданный пользователь.

        """
        if not email:
            raise ValueError('Users must have an Email address')
        if not password:
            raise ValueError('Users must have an Password')
        user: User = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_verified=is_verified,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, first_name: str = "admin", last_name: str = "admin"):
        """
        Создает и сохраняет суперпользователя с указанными данными.

        ### Args:
        - email (`str`): Email суперпользователя.
        - password (`str`): Пароль суперпользователя.
        - first_name (`str`, опционально): Имя суперпользователя.
        - last_name (`str`, опционально): Фамилия суперпользователя.

        ### Returns:
        - `User`: Созданный суперпользователь.

        """
        return self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
            is_verified=True,
        )


class User(AbstractUser):
    """
    Модель пользователя с расширенными полями.

    ### Fields:
    - username (`CharField`, опционально): Имя пользователя.
    - email (`EmailField`): Адрес электронной почты.
    - first_name (`CharField`, опционально): Имя пользователя.
    - last_name (`CharField`, опционально): Фамилия пользователя.
    - role (`CharField`): Пользовательская роль.
    - is_verified (`BooleanField`): Флаг подтверждения.
    - phone_number (`PhoneNumberField`, опционально): Номер телефона.

    ### Meta:
    - verbose_name (`str`): Название в единственном числе.
    - verbose_name_plural (`str`): Название во множественном числе.

    ### Properties:
    - is_admin: Возвращает True, если пользователь администратор.
    - is_moderator: Возвращает True, если пользователь модератор.

    ### Methods:
    - verify(): Подтверждение регистрации.

    """
    class Role(models.TextChoices):
        ADMIN = 'admin', _('администратор')
        MODERATOR = 'moderator', _('модератор')
        USER = 'user', _('авторизованный пользователь')

    username = models.CharField(blank=True, null=True, max_length=128)

    email = models.EmailField(verbose_name=_('адрес электронной почты'), max_length=254, unique=True,)

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    role = models.CharField(verbose_name=_('пользовательская роль'), max_length=10, choices=Role.choices, default=Role.USER)

    is_verified = models.BooleanField(_('is verified'), default=False)

    phone_number = PhoneNumberField(_('номер телефона'), null=True, blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            self.role == 'admin'
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def verify(self) -> 'User':
        """Подтверждения регистрации."""
        if not self.is_verified:
            self.is_verified = True
            self.code = None
            self.save()
        return self
