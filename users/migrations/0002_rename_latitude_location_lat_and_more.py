# Generated by Django 4.2.1 on 2023-05-29 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='latitude',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='longitude',
            new_name='lng',
        ),
    ]
