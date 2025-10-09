import os
from datetime import datetime
from django.db.models import Model, Func
from django.db.models.fields import UUIDField, DateTimeField
from django.db.models import (CharField, ImageField)


class GenRandomUUID(Func):
    """
    Represents the PostgreSQL gen_random_uuid() function.
    """
    function = "gen_random_uuid"
    template = "%(function)s()"  # no args
    output_field = UUIDField()


class UUIDBaseModel(Model):
    id = UUIDField(primary_key=True, db_default=GenRandomUUID(), editable=False)

    class Meta:
        abstract = True


class CreatedBaseModel(UUIDBaseModel):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class CreatedCategoryModel(UUIDBaseModel):
    name = CharField(max_length=155, blank=False)

    def __str__(self):
        return self.name

class CreatedImageModel(UUIDBaseModel):

    @staticmethod
    def upload_to(instance, filename):
        model_name = instance.__class__.__name__.lower()
        filename = os.path.basename(filename)
        date_path = datetime.now().strftime("%Y/%m/%d")
        return f"/{model_name}/{date_path}/{filename}"

    url = ImageField(upload_to=upload_to)


