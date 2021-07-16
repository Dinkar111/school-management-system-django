from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, full_name=None, address=None,
                    phone=None, is_teacher=False, is_student=False):
        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            address=address,
            phone=phone,
            is_teacher=is_teacher,
            is_student=is_student
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            full_name=None,
            address=None,
            phone=None
        )
        user.set_password(password)
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    full_name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        db_table = 'users'
        ordering = ['full_name']
