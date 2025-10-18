from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.db.models import (CharField, TextField, ImageField,
                              ForeignKey, PROTECT, ManyToManyField, PositiveSmallIntegerField,
                              DateTimeField, CASCADE, URLField, TextChoices, FloatField,
                              DecimalField, BooleanField, FileField, JSONField, Sum, PositiveIntegerField)
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from main.models.base import CreatedBaseModel, UUIDBaseModel, SlugBasedModel, MAX_CHAR_LENGTH, OrderNumberBaseModel
from video_encoding.fields import VideoField

NULLABLE = {'blank': True, 'null': True}


def course_upload_path(model, file) -> str:
    model_name = model.__class__.__name__.lower()
    return f'course/{model_name}/%Y/%m/%d/{file}'



class CourseCategory(SlugBasedModel):
    name = CharField(max_length=155)
    total_course_count = PositiveIntegerField(db_default=0)

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ['name']

    def __str__(self):
        return self.name


class Language(UUIDBaseModel):
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
    preview_img = ImageField(upload_to=course_upload_path, **NULLABLE, verbose_name=_("Эскиз"))
    preview_video = FileField(upload_to=course_upload_path, **NULLABLE, verbose_name=_("Превью видео"))
    duration = DecimalField(max_digits=3, decimal_places=1, **NULLABLE, verbose_name=_("Продолжительность"),
                            help_text="Продолжительность в часах")

    # Категории / язык / авторы
    category = ForeignKey('main.CourseCategory', PROTECT, related_name="course")
    language = ForeignKey('main.Language', PROTECT, related_name="course")
    subtitles = ManyToManyField('main.Language', related_name='courses_subtitles')
    authors = ManyToManyField('main.Instructor', related_name='authored_courses', verbose_name=_('Владелецы курса'))
    students = ManyToManyField('users.User', limit_choices_to={'type': 'student'}, related_name='enrolled_courses')

    # Доп. мета
    level = CharField(max_length=25, choices=Level.choices, default=Level.BEGINNER)  # type: ignore
    what_you_will_learn = JSONField(
        default=list,
        verbose_name=_("Чему вы научитесь")
    )
    topics = ManyToManyField('main.Topic', related_name='courses', blank=True, help_text=_("Обзор связанных тем"))

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


class Section(CreatedBaseModel, OrderNumberBaseModel):
    course = ForeignKey('main.Course', CASCADE, related_name='sections')
    title = CharField(max_length=155)
    lectures_count = PositiveSmallIntegerField(default=0)
    # duration = # TODO

    # def duration_summ(self):
    #     return self.lectures.aggregate(total=Sum('duration'))['total'] or 0
    # return Lecture.objects.filter(course=self).aggregate(total=Sum('duration'))['total'] or 0


class Lecture(CreatedBaseModel):
    title = CharField(max_length=155, verbose_name=_('Название курса'))
    section = ForeignKey('main.Section', CASCADE, verbose_name='Курс', related_name='lectures')


class LectureContent(CreatedBaseModel):
    title = CharField(max_length=MAX_CHAR_LENGTH)
    lecture = ForeignKey('main.Lecture', CASCADE, related_name='lecture_contents')
    duration = FloatField(editable=False, null=True)
    video = VideoField(upload_to=course_upload_path, duration_field='duration', verbose_name=_("Видео к урок"))
    file = FileField(
        upload_to=course_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['.jpg', 'jpeg', 'png', '.pdf', '.docx']
            )
        ],
        verbose_name=_("Файл к уроку")
    )


class CourseComment(UUIDBaseModel):
    course = ForeignKey('main.Course', CASCADE, related_name='course_comment')
    user = ForeignKey('users.User', CASCADE, related_name='course_comments')
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
    completion_status = CharField(
        max_length=20,
        choices=CompletionStatus.choices,
        default=CompletionStatus.ENROLLED
    )


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


class CourseRating(CreatedBaseModel):
    course = ForeignKey('main.Course', CASCADE, related_name='rating')
    student = ForeignKey('users.User', CASCADE, related_name='rating')
    rating = FloatField(default=0, validators=[MinValueValidator(3), MaxValueValidator(4.5)])
    reviews = TextField(**NULLABLE)

#
# class StudentFavoriteCourse(CreatedBaseModel):
#     course = ForeignKey('main.Course', CASCADE)
#     student = ForeignKey('users.User', CASCADE)
#     status = BooleanField(default=False)
#
#     class Meta:
#         verbose_name_plural = _("Избранные курсы студента")
