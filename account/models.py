from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.shortcuts import reverse

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

class User(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, unique=False)
    last_name = models.CharField(max_length=100, unique=False)
    pers_code = models.CharField(primary_key=True,max_length=11, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','pers_code']

    objects = myAccountManager()

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    phone_number = models.CharField(max_length=20, unique=False)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    sert_nr = models.CharField(unique=True, max_length=11)
    spec = models.CharField(unique=True, max_length=30)
    free_text = models.TextField(blank=True)

        
class DoctorApplication(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100, unique=False)
    last_name = models.CharField(max_length=100, unique=False)
    pers_code = models.CharField(primary_key=True,max_length=11, unique=True)
    sert_nr = models.CharField(unique=True, max_length=11)
    spec = models.CharField(unique=True, max_length=30)
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


# class Account(AbstractUser):
#     email = models.EmailField(max_length=254, unique=True)
#     name = models.CharField(max_length=254, null=True, blank=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     last_login = models.DateTimeField(null=True, blank=True)
#     date_joined = models.DateTimeField(auto_now_add=True)

#     USERNAME_FIELD = 'email'
#     EMAIL_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = myAccountManager()

#     def get_absolute_url(self):
#         return "/users/%i/" % (self.pk)
#     def get_email(self):
#         return self.email





# class Admin(AbstractBaseUser):
#     email = models.EmailField(verbose_name="email",max_length=60, unique=True)
#     username = models.CharField(max_length=30, unique=True)
#     date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
#     is_admin = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=True)
#     first_name = models.CharField(max_length=100, unique=False)
#     last_name = models.CharField(max_length=100, unique=False)
#     pers_code = models.CharField(primary_key=True,max_length=11, unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username','first_name','last_name','pers_code']

#     objects = myAccountManager()

#     def _str_(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return self.is_admin
    
#     def has_module_perms(self, app_label):
#         return True

#     def get_absolute_url(self):
#         # if self.is_doctor:
#         #     return reverse('dataBase')
#         return reverse('home')

# class Patient(AbstractBaseUser):
#     email = models.EmailField(verbose_name="email",max_length=60, unique=True)
#     username = models.CharField(max_length=30, unique=True)
#     date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     first_name = models.CharField(max_length=100, unique=False)
#     last_name = models.CharField(max_length=100, unique=False)
#     pers_code = models.CharField(primary_key=True,max_length=11, unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username','first_name','last_name','pers_code']

#     objects = myAccountManager()

#     def _str_(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return self.is_admin
    
#     def has_module_perms(self, app_label):
#         return True

#     def get_absolute_url(self):
#         # if self.is_doctor:
#         #     return reverse('dataBase')
#         return reverse('home')




