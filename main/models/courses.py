from django.db.models import (Model, CharField, TextField, ImageField,
                              SlugField, ForeignKey, PROTECT, ManyToManyField, PositiveSmallIntegerField,
                              DateTimeField, CASCADE, PositiveIntegerField)
from django.utils.translation import gettext_lazy as _

from users.models import User
from .base import CreatedBaseModel, CreatedCategoryModel, UUIDBaseModel


class CourseCategory(CreatedCategoryModel):
    pass


class Instructor(User):
    name = CharField(max_length=150, null=False)
    bio = TextField()
    photo = ImageField(upload_to='instructor/%Y/%m/%d')
    follow = ForeignKey('main.SocialLink', CASCADE, related_name='instructor')


class Course(Model):
    title = CharField(max_length=255)
    slug = SlugField(unique=True)
    thumbnail = ImageField(upload_to="courses/thumbnails/%Y/%m/%d")
    category = ForeignKey('main.CourseCategory', PROTECT, related_name="courses")
    instructor = ManyToManyField('main.Instructor', related_name='corses')
    description = TextField()
    duration_week = PositiveSmallIntegerField(default=1)

    quizzes_count = PositiveSmallIntegerField(default=0)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)


class Lesson(CreatedBaseModel):
    lessons_count = PositiveSmallIntegerField(default=1)


class Comment(UUIDBaseModel):
    user = ForeignKey('main.Student', CASCADE, related_name='comments')
    name = CharField(max_length=55)
    comment_text = TextField()
    posted_at = DateTimeField(auto_now_add=True)


class FAQ(CreatedBaseModel):
    question = CharField(
        max_length=255,
        verbose_name=_("Question"),
        help_text=_("Введите вопрос")
    )
    answer = TextField(
        verbose_name=_("Answer"),
        help_text=_("Введите ответ на вопрос")
    )

    order = PositiveIntegerField(
        default=0,
        verbose_name=_("Display order"),
        help_text=_("Порядок отображения в списке FAQ")
    )

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ["order", "id"]

    def __str__(self):
        return self.question
