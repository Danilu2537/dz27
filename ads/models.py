from django.core.validators import MinLengthValidator
from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(10)])
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()
    category = models.ForeignKey('ads.Category', on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='ads_images', blank=True, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


    def __str__(self):
        return self.name


class Selection(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    items = models.ManyToManyField('ads.Ad')

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=10, validators=[MinLengthValidator(5)], unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


    def __str__(self):
        return self.name
