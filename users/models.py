from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

# Модель пользователя
class AppUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    role = models.ForeignKey(
        'access.Role',
        on_delete=models.SET_NULL,
        null=True
    )

    USERNAME_FIELD = 'email'
    objects = UserManager()