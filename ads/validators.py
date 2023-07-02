from rest_framework.exceptions import ValidationError


def check_is_False(value):
    if value:
        raise ValidationError('Значение при создании не может быть True!')
