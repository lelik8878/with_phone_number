from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Users must have a phone number')
        phone_number = self.model(phone_number=phone_number, **extra_fields)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь с идентификацией по номеру телефона"""
    phone_number = models.CharField(max_length=15, unique=True, verbose_name='Номер телефона')
    nickname = models.CharField(max_length=100, verbose_name='Ник')
    main_image = models.ImageField(upload_to='media/', null=True, blank=True,
                                   default='media/no_photo.png', verbose_name='Главное изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='В штате')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.phone_number} --- {self.nickname}'


class Profile(models.Model):
    """Профиль пользователя"""
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Профайл'
        verbose_name_plural = 'Профайлы'

    def __str__(self):
        return f'{self.name} --- {self.surname}'


class Image(models.Model):
    """Дополнительные изображения"""
    additional_image = models.ImageField(upload_to='media/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
