from django.db.models import (CharField, ForeignKey, TextField, CASCADE, PROTECT, BooleanField)

from main.models.base import CreatedCategoryModel, CreatedImageModel, CreatedBaseModel


class BlogCategory(CreatedCategoryModel):
    pass


class BlogImage(CreatedImageModel):
    pass


class Blog(CreatedBaseModel):
    title = CharField(max_length=255, blank=False)
    description = TextField()
    archived = BooleanField(db_default=False)
    images = ForeignKey('BlogImage', CASCADE, related_name='blog')
    created_by = ForeignKey('auth.User', PROTECT, editable=False)

    def __str__(self):
        return self.title
