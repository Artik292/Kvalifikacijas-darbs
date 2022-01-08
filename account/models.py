from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.shortcuts import reverse
from django.core.validators import MaxValueValidator, MinValueValidator,RegexValidator
from django.contrib import messages
from django.contrib.auth.models import PermissionsMixin

YES_NO = (

    ('yes','yes'),
    ('no','no'),
    ('cannot_say','cannot say'),
)

class myAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, pers_code, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not first_name:
            raise ValueError("Users must have an first name")
        if not last_name:
            raise ValueError("Users must have an last name")
        if not pers_code:
            raise ValueError("Users must have an personal code")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            pers_code=pers_code,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, pers_code, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            pers_code=pers_code,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, unique=False)
    last_name = models.CharField(max_length=100, unique=False)
    pers_code = models.CharField(primary_key=True,max_length=11, validators=[RegexValidator(regex='^.{11}$', message='Length has to be 11.', code='nomatch')], unique=True)

    objects = myAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','pers_code']

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

class Patient(models.Model):
    USERNAME_FIELD = 'user'
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    regions = models.CharField(max_length=100,blank=False)
    uses_medicaments = models.CharField(max_length=10,choices=YES_NO,default='no')
    medicaments = models.TextField(blank=True)
    uses_alcohol = models.CharField(max_length=10,choices=YES_NO,default='no')
    is_smoking = models.CharField(max_length=10,choices=YES_NO,default='no')
    are_chronic_diseases = models.CharField(max_length=10,choices=YES_NO,default='no')
    chronic_diseases = models.TextField(blank=True)


class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key = True, on_delete = models.CASCADE)
    sert_nr = models.CharField(unique=True, max_length=11,null=True)
    spec = models.CharField(max_length=30)
    free_text = models.TextField(blank=True)
    accepted_analysis_count = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
        
class DoctorApplication(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",max_length=60, unique=True)
    is_doctor = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100, unique=False)
    last_name = models.CharField(max_length=100, unique=False)
    pers_code = models.CharField(primary_key=True,max_length=11, validators=[RegexValidator(regex='^.{11}$', message='Length has to be 11.', code='nomatch')], unique=True)
    sert_nr = models.CharField(unique=True, max_length=11)
    spec = models.CharField(max_length=30)
    free_text = models.TextField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','pers_code','sert_nr','spec']

    objects = myAccountManager()

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True





