from django.db.models import UUIDField, DateField, EmailField, BooleanField, CharField

from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)

from main.models import UUIDBaseModel


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError()
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, UUIDBaseModel):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    email = EmailField(unique=True)
    username = CharField(max_length=150, unique=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    created_at = DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # Говорит используй поле emal для login вместо username
    REQUIRED_FIELDS = ('username',)
    objects = UserManager()

    def __str__(self):
        return self.email
