from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUsers(AbstractUser):
    class UserType(models.TextChoices):
        EMPLOYER = 'employer', '👔 Работодатель'
        JOB_SEEKER = 'seeker', '🔍 Соискатель'

    user_type = models.CharField(
        'Тип пользователя',
        max_length=10,
        choices=UserType.choices,
        default=UserType.JOB_SEEKER
    )
    phone = models.CharField('Телефон', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} ({self.get_user_type_display()})'


class Profile(models.Model):
    user = models.OneToOneField(  # ← назови user, а не profile
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    city = models.CharField('Город', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль {self.user.username}'


