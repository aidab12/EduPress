from django.db.models import (Model, CharField, TextField, ImageField,
                              SlugField, ForeignKey, PROTECT, ManyToManyField, PositiveSmallIntegerField,
                              DateTimeField, CASCADE, PositiveIntegerField, URLField, TextChoices)
from django.utils.translation import gettext_lazy as _

from users.models import User
from .base import CreatedBaseModel, CreatedCategoryModel, UUIDBaseModel


class CourseCategory(CreatedCategoryModel):
    pass


class Course(CreatedBaseModel):
    title = CharField(max_length=255)
    thumbnail = ImageField(upload_to="courses/thumbnails/%Y/%m/%d")
    category = ForeignKey('main.CourseCategory', PROTECT, related_name="courses")
    instructor = ManyToManyField('main.Instructor', related_name='corses')
    description = TextField()
    duration_week = PositiveSmallIntegerField(default=1)
    quizzes_count = PositiveSmallIntegerField(default=0)



class CourseContent(CreatedBaseModel):
    course = ForeignKey('main.Course', CASCADE, 'course_content')
    CONTENT_TYPE_CHOICES = [
    ('text', 'Text'),
    ('video', 'Video'),
    ('quiz', 'Quiz'),
    ]
    content_type = CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    lesson_content = PositiveIntegerField()
    video_url = URLField(max_length=255)


class Enrollment(CreatedBaseModel): # (Запись на курс)

    class CompletionStatus(TextChoices):
        ENROLLED = "enrolled", _("Зачислен")
        IN_PROGRESS = "in_progress", _("Проходит")
        COMPLETED = "completed", _("Завершил")
        CANCELLED = "cancelled", _("Отменено")

    student = ForeignKey('users.Student', CASCADE)
    course = ForeignKey('main.Course', CASCADE, 'enrollments')
    enrollment_date = DateTimeField(auto_now_add=True) # дата зачисления
    completion_status = CharField(
        max_length=20,
        choices=CompletionStatus.choices,
        default=CompletionStatus.ENROLLED
    )


class Quiz(CreatedBaseModel):
    course = ForeignKey('main.Course', CASCADE, 'quizzes')
    quiz_name = CharField(max_length=255)
    description = TextField(blank=True)
    totalMarks = PositiveSmallIntegerField(default=100) #максимальное количество баллов

class CourseProgress(CreatedBaseModel):
    pass


class CourseResult:
    user = ForeignKey('main.Student', CASCADE, 'course_result')
    course = ForeignKey('main.Course', CASCADE)
    quiz = ForeignKey('main.Quiz', CASCADE, related_name='results')
    score = PositiveSmallIntegerField(default=0)

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
