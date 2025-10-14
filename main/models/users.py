from django.db.models import (CharField, TextField, ImageField,
                              ForeignKey, CASCADE, URLField,
                              OneToOneField, TextChoices)
from django.db.models.constraints import UniqueConstraint

from main.models import UUIDBaseModel
from users.models import User


class Instructor(User):
    skills = CharField(max_length=255)
    photo = ImageField(upload_to='instructor/%Y/%m/%d')
    bio = TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name} '


