import os
from datetime import datetime
from django.db.models import Model, Func, SlugField
from django.db.models import (CharField, ImageField, TextChoices, URLField, UUIDField, DateTimeField, PositiveSmallIntegerField)
from django.utils.text import slugify


MAX_CHAR_LENGTH = 155

class GenRandomUUID(Func):
    """
    Represents the PostgreSQL gen_random_uuid() function.
    """
    function = "gen_random_uuid"
    template = "%(function)s()"  # no args
    output_field = UUIDField()


class UUIDBaseModel(Model):
    id = UUIDField(
        primary_key=True,
        db_default=GenRandomUUID(),
        editable=False,
    )

    class Meta:
        abstract = True


class CreatedBaseModel(UUIDBaseModel):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class CreatedImageModel(UUIDBaseModel):

    @staticmethod
    def upload_to(instance, filename):
        model_name = instance.__class__.__name__.lower()
        filename = os.path.basename(filename)
        date_path = datetime.now().strftime("%Y/%m/%d")
        return f"{model_name}/{date_path}/{filename}"

    image = ImageField(upload_to=upload_to)

    class Meta:
        abstract = True


class SlugBasedModel(UUIDBaseModel):
    slug = SlugField(unique=True, editable=False)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            sourse = getattr(self, 'name', None) or getattr(self, 'title', None)

            if sourse:
                self.slug = slugify(sourse, allow_unicode=True)

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.slug


class SocialLinkBase(Model):
    class Platform(TextChoices):
        FACEBOOK = 'facebook', 'Facebook'
        INSTAGRAM = 'instagram', 'Instagram'
        YOUTUBE = 'youtube', 'YouTube'
        PINTEREST = 'pinterest', 'Pinterest'
        X = 'x', 'X'

    platform = CharField(
        max_length=20,
        choices=Platform.choices,
    )
    url = URLField(max_length=255)

    class Meta:
        abstract = True


class OrderNumberBaseModel(Model):
    order_number = PositiveSmallIntegerField(default=1)

    class Meta:
        abstract = True