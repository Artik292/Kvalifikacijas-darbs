from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = Account
        fields = ("email","username","first_name","last_name","pers_code","is_doctor","password1","password2")
