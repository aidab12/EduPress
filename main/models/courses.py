from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.db.models import (CharField, TextField, ImageField,
                              ForeignKey, PROTECT, ManyToManyField, PositiveSmallIntegerField,
                              DateTimeField, CASCADE, URLField, TextChoices, FloatField,
                              DecimalField, BooleanField, FileField, JSONField, Sum, PositiveIntegerField)
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from .base import CreatedBaseModel, UUIDBaseModel, SlugBasedModel

from video_encoding.fields import VideoField

NULLABLE = {'blank': True, 'null': True}


def course_upload_path(model, file) -> str:
    return f'course/{model.title}/{file}'


def lesson_upload_path(model, file) -> str:
    return f'lesson/{model.title}/{file}'


class CourseCategory(SlugBasedModel):
    name = CharField(max_length=155)
    total_course_count = PositiveIntegerField(db_default=0)

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ['name']

    def __str__(self):
        return self.name


class Language(UUIDBaseModel):  # TODO add fixtures
    code = CharField(max_length=15, unique=True)
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(CreatedBaseModel, SlugBasedModel):
    class Level(TextChoices):
        BEGINNER = 'beginner', _('Начальный')
        INTERMEDIATE = 'intermediate', _('Средний')
        PROFESSIONAL = 'professional', _('Профессиональный')

    # Основные
    title = CharField(max_length=255, unique=True, verbose_name=_("Название курса"))
    description = CKEditor5Field(verbose_name=_("Описание курса"))
    overview = CharField(max_length=500, verbose_name=_("Краткое описание"))  # Краткий обзор курса

    # Мультимедиа / превью
    preview_img = ImageField(upload_to=course_upload_path, verbose_name=_("Эскиз"))
    preview_video = FileField(upload_to=course_upload_path, **NULLABLE, verbose_name=_("Превью видео"))
    duration = DecimalField(max_digits=3, decimal_places=1, verbose_name=_("Продолжительность"),
                            help_text="Продолжительность в часах")

    # Категории / язык / авторы
    category = ForeignKey('main.CourseCategory', PROTECT, related_name="course")
    language = ForeignKey('main.Language', PROTECT, related_name="course")
    subtitles = ForeignKey('main.Language', PROTECT, **NULLABLE, related_name='course_sub')
    authors = ManyToManyField('main.Instructor', related_name='courses', verbose_name='Владелец курса')
    students = ManyToManyField('main.User', limit_choices_to={'type': 'student'}, related_name='courses')

    # Доп. мета
    level = CharField(max_length=25, choices=Level.choices, default=Level.BEGINNER)  # type: ignore
    what_you_will_learn = JSONField(
        default=list,
        verbose_name=_("Чему вы научитесь")
    )
    topics = ManyToManyField('main.Topic', related_name='courses', help_text=_("Обзор связанных тем"))

    # Цена
    is_free = BooleanField(default=False)
    price = DecimalField(max_digits=10, decimal_places=2)

    # Управление публикацией
    is_published = BooleanField(default=False, verbose_name=_("Опубликован"))

    # is_featured = BooleanField(**NULLABLE, editable=False, verbose_name=_("Рекомендованный"))

    def course_rating(self):
        course_rating = CourseRating.objects.filter(course=self).aggregate(avg_rating=models.Avg('rating'))
        return course_rating['avg_rating']

    def course_rating_summ(self):
        return CourseRating.objects.filter(course=self).count()

    def total_enrolled_students(self):
        return self.enrollments.count()

        # total_enrolled_students = Enrollment.objects.filter(course=self).count()
        # return total_enrolled_students

    def course_authors(self):
        return self.authors.all()

    class Meta:
        verbose_name = _("Курс")
        verbose_name_plural = _("Курсы")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Section(CreatedBaseModel):
    course = ForeignKey('main.Course', CASCADE, related_name='sections')
    order_number = PositiveSmallIntegerField(default=1)
    title = CharField(max_length=155)
    lectures_count = PositiveSmallIntegerField(default=0)

    # duration = # TODO

    # def duration_summ(self):
    #     return self.lectures.aggregate(total=Sum('duration'))['total'] or 0
    # return Lecture.objects.filter(course=self).aggregate(total=Sum('duration'))['total'] or 0


class Lecture(CreatedBaseModel):
    title = CharField(max_length=155, verbose_name='Название курса')
    # description = CKEditor5Field(verbose_name='Описание урока') ?
    preview = ImageField(upload_to=lesson_upload_path, verbose_name='Превью урока', **NULLABLE)
    video_link = URLField(verbose_name='Ссылка на видео', **NULLABLE)
    section = ForeignKey('main.Section', CASCADE, verbose_name='Курс', related_name='lectures')
    lesson_author = FileField(
        upload_to=lesson_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['.jpg', 'jpeg', 'png', '.pdf', '.mp4', '.mov', '.avi']
            )
        ]
    )


class LessonContent(CreatedBaseModel):
    created_by = ForeignKey('main.Instructor', PROTECT, related_name='lesson_contents')
    lesson = ForeignKey('main.Lesson', CASCADE, related_name='lesson_contents')
    video_url = URLField(max_length=255)


class LessonComment(UUIDBaseModel):
    lesson = ForeignKey('main.Lesson', CASCADE, related_name='lesson_comment')
    user = ForeignKey('users.User', CASCADE, related_name='lesson_comments')
    comment_text = TextField()
    created_at = DateTimeField(auto_now_add=True)


class Topic(UUIDBaseModel):
    name = CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Enrollment(CreatedBaseModel):  # (Запись на курс)

    class CompletionStatus(TextChoices):
        ENROLLED = "enrolled", _("Зачислен")
        IN_PROGRESS = "in_progress", _("Проходит")
        COMPLETED = "completed", _("Завершил")
        CANCELLED = "cancelled", _("Отменено")

    student = ForeignKey('users.User', CASCADE, related_name='enrollments', limit_choices_to={'type': 'student'})
    course = ForeignKey('main.Course', CASCADE, related_name='enrollments')
    # enrollment_date = DateTimeField(auto_now_add=True)  # дата зачисления
    completion_status = CharField(
        max_length=20,
        choices=CompletionStatus.choices,  # ignore: type
        default=CompletionStatus.ENROLLED
    )
    # enrolled_time = DateTimeField(auto_now_add=True)


class CourseTest(CreatedBaseModel):  # TODO ?
    course = ForeignKey('main.Course', CASCADE, 'quizzes')
    test_name = CharField(max_length=255)
    description = TextField(blank=True)
    total_ball = PositiveSmallIntegerField(default=0,
                                           validators=[MaxValueValidator(100)])  # максимальное количество баллов


# class CourseProgress(CreatedBaseModel):
#     pass


class CourseResult(CreatedBaseModel):
    user = ForeignKey('users.User', CASCADE, related_name='course_result')
    course = ForeignKey('main.Course', CASCADE)
    test_result = ForeignKey('main.CourseTest', CASCADE, related_name='results')
    score = PositiveSmallIntegerField(default=0)


class CourseRating(UUIDBaseModel, CreatedBaseModel):
    course = ForeignKey('main.Course', CASCADE, related_name='rating')
    student = ForeignKey('users.User', CASCADE, related_name='rating')
    rating = FloatField(default=0, validators=[MinValueValidator(3), MaxValueValidator(4.5)])
    reviews = TextField(null=True)
    # created_at = DateTimeField(auto_now_add=True)

#
# class StudentFavoriteCourse(CreatedBaseModel):
#     course = ForeignKey('main.Course', CASCADE)
#     student = ForeignKey('users.User', CASCADE)
#     status = BooleanField(default=False)
#
#     class Meta:
#         verbose_name_plural = _("Избранные курсы студента")
