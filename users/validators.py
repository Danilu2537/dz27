from datetime import date

from rest_framework.exceptions import ValidationError


def check_age(value):
    today = date.today()
    age = (today.year - value.year) - ((today.month, today.day) < (value.month, value.day))
    if age < 9:
        raise ValidationError('Возраст не может быть меньше 9 лет!')
