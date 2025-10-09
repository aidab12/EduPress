from django.db.models import TextField, CharField, EmailField
from main.models import CreatedBaseModel


class AboutCompany(CreatedBaseModel):
    title = TextField()
    text = TextField()
    email = EmailField()
    phone1 = CharField()
    phone2 = CharField()