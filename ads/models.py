from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.PositiveIntegerField()
    category = models.ForeignKey('ads.Category', on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='ads_images', blank=True, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author.username,
            "description": self.description,
            "price": self.price,
            "is_published": self.is_published,
            "category": self.category.name,
            "image": self.image.url if self.image else None,
        }

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

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def __str__(self):
        return self.name
