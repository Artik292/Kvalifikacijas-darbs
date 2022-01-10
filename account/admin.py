from django.contrib import admin,messages
from django.contrib.auth.models import Group
from django.forms.fields import EmailField
from account.models import User, Patient, Doctor, DoctorApplication
from dicom_viewer.models import Dicom
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .forms import PatientInfoForm, UserRegistrationForm


class DoctorApplicationAdmin(admin.ModelAdmin):

    readonly_fields = ['password']

    actions = ['Approve']
    list_display = ('email','pers_code','spec','sert_nr')

    fieldsets = (
        ("Users data", {
            'fields': ("email","pers_code","first_name","last_name","password")
        }),
        ("Doctors data",{
            'fields':("spec","sert_nr","free_text")
        }),

    )

    def Approve(self,request,queryset):
        user = queryset.first()
        for user in queryset:
            try:
                #check if this doctor already exists
                if User.objects.filter(email=user.email).exists() or User.objects.filter(pers_code=user.pers_code).exists():
                    self.message_user(request, "User with this email or personal code already exists", level=messages.ERROR)
                    return
            except:
                #data transfer from one table to anothers
                newUser = User.objects.create(first_name=user.first_name,last_name=user.last_name,pers_code=user.pers_code,email=user.email,password=user.password,is_doctor=user.is_doctor)
                newUser.save()
                newDoctor = Doctor.objects.create(user=newUser,sert_nr=user.sert_nr,free_text=user.free_text,spec=user.spec)
                newDoctor.save()
                messages.success(request, 'New user and doctor was created.')
        queryset.delete()
    #admin cant create new doctor applications
    def has_add_permission(self, request, obj=None):
        return False


class PatientChangeForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ('user',)

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user','regions','chronic_diseases')

    form = PatientInfoForm

    readonly_fields = ['user']

    fieldsets = (
        ("Based on user", {
            'fields': ("user",)
        }),
        ("Patients info",{
            'fields': ("regions","is_smoking","uses_alcohol","uses_medicaments","medicaments","are_chronic_diseases","chronic_diseases")
        }),
    )

    def delete_queryset(self, request, queryset):
        patient = queryset.first()
        for patient in queryset:
            User.objects.get(patient=patient).delete()
        queryset.delete()

    def has_add_permission(self, request, obj=None):
        return False

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user','spec','sert_nr')
    readonly_fields = ['accepted_analysis_count']

    def delete_queryset(self, request, queryset):
        doctor = queryset.first()
        for doctor in queryset:
            user = User.objects.get(doctor=doctor)
            user.delete()
            if Dicom.objects.filter(study_doctor=user).exists():
                dicom = Dicom.objects.get(study_doctor=user)
                dicom.medical_verdict = ''
                dicom.status = 'Uploaded'
        queryset.delete()

    def has_add_permission(self, request, obj=None):
        return False

class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_admin')

    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserRegistrationForm
    list_display = ('email','pers_code')
    list_filter = ('is_admin',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('pers_code','first_name','last_name')}),
        ('Role', {'fields': ('is_admin','is_patient','is_doctor')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ("email","first_name","last_name","pers_code",'is_admin','is_patient','is_doctor',"password1","password2")}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    
    def save_model(self, request, obj, form, change):
        if (obj.is_patient and obj.is_doctor):
            messages.set_level(request, messages.ERROR)
            messages.error(request, "User cannot have multiple roles at the same time")
            return
        else:
            code = obj.pers_code
            code_lowercase = code.lower()
            contains_letters = code_lowercase.islower()
            if contains_letters:
                messages.set_level(request, messages.ERROR)
                messages.error(request, "Pers code can only contain numbers")
                return
            if obj.is_admin or obj.is_staff or obj.is_superuser:
                obj.is_patient = False
                obj.is_doctor = False
                obj.is_admin = True
                obj.is_staff = True
                obj.is_superuser = True
                if Doctor.objects.filter(user=obj).exists():
                    Doctor.objects.filter(user=obj).delete()
                if Patient.objects.filter(user=obj).exists():
                    Patient.objects.filter(user=obj).delete()
            else: 
                if obj.is_patient:
                    if not Patient.objects.filter(user=obj).exists():
                        Patient.objects.create(user=obj).save()
                    if Doctor.objects.filter(user=obj).exists():
                        Doctor.objects.filter(user=obj).delete()
                if obj.is_doctor: 
                    if not Doctor.objects.filter(user=obj).exists():
                        Doctor.objects.create(user=obj).save()
                    if Patient.objects.filter(user=obj).exists():
                        Patient.objects.filter(user=obj).delete()

            obj.save()
        


admin.site.site_header = "Admin Dashboard"
admin.site.register(User,UserAdmin)
admin.site.register(Patient,PatientAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(DoctorApplication,DoctorApplicationAdmin)
admin.site.unregister(Group)
