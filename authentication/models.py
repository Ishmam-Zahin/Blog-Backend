from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class BlogUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, user_name, email, password = None, **kwargs):
        if not email:
            raise ValueError("user must have an email address")
        
        if not password:
            raise ValueError("user must enter an password")
        
        kwargs.pop('is_admin', None)
        kwargs.pop('is_staff', None)
        kwargs.pop('is_active', None)
        kwargs.pop('last_login', None)
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            user_name = user_name,
            email = self.normalize_email(email),
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, user_name, email, avatar_link = None, password = None):
        if not email:
            raise ValueError("user must have an email address")
        
        if not password:
            raise ValueError("user must enter an password")
        
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            user_name = user_name,
            avatar_link = avatar_link,
            email = self.normalize_email(email)
        )
        user.is_admin = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user
        

class BlogUser(AbstractBaseUser):
    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GenderChoices, default=GenderChoices.MALE.value)
    age = models.IntegerField(default=-1)
    avatar_link = models.URLField(max_length=500, blank=True, null=True)
    user_name = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    USERNAME_FIELD = 'user_name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = BlogUserManager()

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_level):
        return self.is_admin
    
    def __str__(self):
        return self.user_name
