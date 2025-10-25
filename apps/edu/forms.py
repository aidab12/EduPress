from django.forms import CharField, Form, PasswordInput


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)