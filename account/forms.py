from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Patient, Doctor, User, DoctorApplication
from django.contrib.auth import authenticate

class PatientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email","first_name","last_name","pers_code","password1","password2")

    @transaction.atomic()
    def save(self):
        user = super().save()
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.is_patient = True
        user.save()
        patient = Patient.objects.create(user=user)
        patient.save()
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