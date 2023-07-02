# Generated by Django 4.2.1 on 2023-07-02 19:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_birth_date_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.RegexValidator(inverse_match=True, message='Почта не должна быть rambler.ru', regex='rambler.ru')]),
        ),
    ]
