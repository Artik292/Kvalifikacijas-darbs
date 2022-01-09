from django.test import TestCase
from .forms import PatientRegistrationForm, PatientInfoForm, UserRegistrationForm, ApplicationForm, AccountAuthenticationForm, UpdatePatientInfo
from .models import User, Patient, Doctor
from django.contrib.auth import authenticate

class UserTestCase(TestCase):
    
    def test_patient_registration_form1(self):
        form_data = {
            "first_name":"Ēriks",
            "last_name":"Cvetkovs",
            "pers_code":"16060021557",
            "email":"cvetkov.erik@gmail.com",
            "password1":"DatorikasFakultate2022!",
            "password2":"DatorikasFakultate2022!"
        }
        form = PatientRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        if form.errors:
            print(form.errors.as_text())
            print('**********************************************')

    def test_patient_registration_form2(self):
        form_data = {
            "first_name":"",
            "last_name":"",
            "pers_code":"",
            "email":"",
            "password1":"",
            "password2":""
        }
        form = PatientRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        if form.errors:
            print(form.errors.as_text())
            print('**********************************************')


    def test_patient_registration_form3(self):
        form_data = {
            "first_name":"Aleksejs",
            "last_name":"Demidovs",
            "pers_code":"21039921334",
            "email":"ad.com",
            "password1":"DatorikasFakultate2022!",
            "password2":"DatorikasFakultate2022!"
        }
        form = PatientRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        if form.errors:
            print(form.errors.as_text())
            print('**********************************************')

    def test_patient_registration_form4(self):
        form_data = {
            "first_name":"Ēriks",
            "last_name":"Cvetkovs",
            "pers_code":"160600",
            "email":"cvetkov.erik@gmail.com",
            "password1":"DatorikasFakultate2022!",
            "password2":"DatorikasFakultate2022!"
        }
        form = PatientRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        if form.errors:
            print(form.errors.as_text())
            print('**********************************************')

    def test_patient_registration_form5(self):
        form_data = {
            "first_name":"Ēriks",
            "last_name":"Cvetkovs",
            "pers_code":"16060021557777",
            "email":"cvetkov.erik@gmail.com",
            "password1":"DatorikasFakultate2022!",
            "password2":"DatorikasFakultate2022!"
        }
        form = PatientRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        if form.errors:
            print(form.errors.as_text())
            print('**********************************************')

    def test_patient_registration_form6(self):
        form_data = {
            "first_name":"Ēriks",
            "last_name":"Cvetkovs",
            "pers_code":"11116666776",
            "email":"pac@pac.com",
            "password1":"DatorikasFakultate2022!",
            "password2":"DatorikasFakultate2022!"
        }
        form = PatientRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        if form.errors:
            print(form.errors.as_text())
            print('**********************************************')

    def test_patient_information_form7(self):
        form_data = {
            "regions":"",
            "uses_medicaments":"no",
            "medicaments":"",
            "uses_alcohol":"no",
            "is_smoking":"no",
            "are_chronic_diseases":"no",
            "chronic_diseases":"",
        }
        form = PatientInfoForm(data=form_data)
        self.assertFalse(form.is_valid())
        if form.errors:
            print(form.errors.as_text())
            print('**********************************************')
        
    def test_user_auth_form8(self):
        user = User.objects.create(email='user@user.com')
        user.set_password('DatorikaFakultate2021!')
        user.save()
        user = authenticate(email='user@user.com', password='DatorikaFakultate2021!')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_user_auth_form9(self):
        user = User.objects.create(email='user@user.com')
        user.set_password('DatorikaFakultate2021!')
        user.save()
        user = authenticate(email='user@user', password='DatorikaFakultate2021!')
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_user_auth_form10(self):
        user = User.objects.create(email='user@user.com')
        user.set_password('DatorikaFakultate2021!')
        user.save()
        user = authenticate(email='', password='')
        self.assertFalse((user is not None) and user.is_authenticated)