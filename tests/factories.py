import factory

from ads.models import Category, Ad
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('sentence', nb_words=4)
    slug = factory.Faker('ean', length=8)


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text')
    price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
