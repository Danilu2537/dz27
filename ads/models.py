from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=255)
    is_published = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "description": self.description,
            "price": self.price,
            "address": self.address,
            "is_published": self.is_published
        }

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def __str__(self):
        return self.name
