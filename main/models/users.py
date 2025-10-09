from django.db.models import (CharField, TextField, ImageField,
                              ForeignKey, CASCADE, URLField,
                              OneToOneField)
from django.db.models.constraints import UniqueConstraint

from main.models import UUIDBaseModel
from users.models import User


class Student(User):
    pass


class Instructor(User):
    name = CharField(max_length=150, blank=False, null=False)
    bio = TextField()
    photo = ImageField(upload_to='instructor/%Y/%m/%d')


class SocialLink(UUIDBaseModel):
    PLATFOR_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('pinterest', 'Pinterest'),
        ('x', 'X'),
    ]

    instructor = OneToOneField('main.Instructor', CASCADE, related_name='social_links')
    platform = CharField(max_length=20, choices=PLATFOR_CHOICES)
    url = URLField(max_length=255)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['instructor', 'platform'], name='unique_user_platform')
        ]
