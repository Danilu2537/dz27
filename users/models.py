from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import TextChoices

from users.validators import check_age


class UserRoles(TextChoices):
    MEMBER = 'member', 'Пользователь'
    ADMIN = 'admin', 'Администратор'
    MODERATOR = 'moderator', 'Модератор'


class User(AbstractUser):
    locations = models.ManyToManyField('Location')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)
    birth_date = models.DateField(validators=[check_age], null=True, blank=True)
    email = models.EmailField(validators=[RegexValidator(
        regex=r'rambler.ru',
        message='Почта не должна быть rambler.ru',
        inverse_match=True
    )], unique=True)

    def save(self, *args, **kwargs):
        self.set_password(raw_password=self.password)
        self.check_password(raw_password=self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name
