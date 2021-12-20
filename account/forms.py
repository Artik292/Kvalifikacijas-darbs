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


# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

#     class Meta:
#         model = Patient
#         fields = ("email","username","first_name","last_name","pers_code","password1","password2")


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