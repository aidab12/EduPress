from django.db.models import (CharField, ForeignKey, PROTECT, BooleanField, ImageField)
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from .base import CreatedBaseModel, SlugBasedModel, MAX_CHAR_LENGTH


class BlogCategory(SlugBasedModel):
    name = CharField(max_length=MAX_CHAR_LENGTH)

    class Meta:
        verbose_name = _('Категория Блога')
        verbose_name_plural = _('Категории Блога')

    def __str__(self):
        return self.name


class Blog(CreatedBaseModel):
    title = CharField(max_length=255, blank=False)
    image = ImageField(upload_to='blogs/%Y/%m/%d')
    description = CKEditor5Field()
    archived = BooleanField(db_default=False)
    created_by = ForeignKey('users.User', PROTECT, editable=False)
    category = ForeignKey('main.BlogCategory', PROTECT, related_name='blogs')

    class Meta:
        verbose_name = _('Болг')
        verbose_name_plural = _('Блоги')

    def __str__(self):
        return self.title
