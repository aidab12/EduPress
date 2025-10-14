from django.db.models import TextField, CharField, EmailField, ForeignKey, CASCADE, PositiveIntegerField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from location_field.models.plain import PlainLocationField

from main.models import CreatedBaseModel, UUIDBaseModel, SocialLinkBase


class AboutCompany(UUIDBaseModel):
    title = CharField(max_length=255)
    text = CKEditor5Field()
    email = EmailField()
    phone1 = CharField(max_length=50)
    phone2 = CharField(max_length=50, blank=True, null=True)
    address = CharField(max_length=255)
    city = CharField(max_length=255)
    location = PlainLocationField(based_fields=['city'], zoom=7)

    def __str__(self):
        return self.title


class CompanySocialLink(SocialLinkBase):
    about_company = ForeignKey(
        'main.AboutCompany',
        CASCADE,
        related_name='social_links'
    )


class CompanyFAQ(CreatedBaseModel):
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
