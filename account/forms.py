from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db.models.enums import Choices
from django.forms import widgets
from .models import Patient, Doctor, User, DoctorApplication
from django.contrib.auth import authenticate

class PatientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email","first_name","last_name","pers_code","password1","password2")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    @transaction.atomic()
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.is_patient = True
        user.set_password(self.cleaned_data["password1"])
        if commit:
            patient = Patient.objects.create(user=user)
            patient.save()
            user.save()
        return user

class PatientInfoForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ("regions","uses_medicaments","uses_alcohol","is_smoking","are_chronic_diseases","chronic_diseases","medicaments")

        widgets = {
            'uses_medicaments' : forms.Select(attrs={'class':'form-select form-select-lg select'}),
            'uses_alcohol' : forms.Select(attrs={'class':'form-select form-select-lg'}),
            'is_smoking' : forms.Select(attrs={'class':'form-select form-select-lg'}),
            'are_chronic_diseases' : forms.Select(attrs={'class':'form-select form-select-lg select'}),
        }

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email","first_name","last_name","pers_code","password1","password2")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    @transaction.atomic()
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if user.is_patient:
            patient = Patient.objects.create(user=user)
            patient.save()
        if user.is_doctor:
            doctor = Doctor.objects.create(user=user)
            doctor.save()
        if commit:
            user.save()
        return user
    

class ApplicationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = DoctorApplication
        fields = ("email","first_name","last_name","pers_code","password1","password2","sert_nr","spec","free_text")
    
    def clean(self):
        cd = self.cleaned_data
        email = cd.get('email')
        pers_code = cd.get('pers_code')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "User with this Email already exists.")
        if User.objects.filter(pers_code=pers_code).exists():
            self.add_error('pers_code', "User with this Pers code already exists.")
        return cd


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class UpdatePatientInfo(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email","first_name","last_name","pers_code")