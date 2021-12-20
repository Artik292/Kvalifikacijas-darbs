from django.contrib import admin
from django.contrib.auth.models import Group
from account.models import User, Patient, Doctor, DoctorApplication


class DoctorApplicationAdmin(admin.ModelAdmin):

    actions = ['Approve']

    def Approve(self,request,queryset):
        user = queryset.first()
        for user in queryset:
            newUser = User.objects.create(first_name=user.first_name,last_name=user.last_name,pers_code=user.pers_code,email=user.email,password=user.password,is_doctor=user.is_doctor)
            newUser.save()
            newDoctor = Doctor.objects.create(user=newUser,sert_nr=user.sert_nr,free_text=user.free_text,spec=user.spec)
            newDoctor.save()
        queryset.delete()

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user',)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user',)
        


admin.site.site_header = "Admin Dashboard"
admin.site.register(User)
admin.site.register(Patient,PatientAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(DoctorApplication,DoctorApplicationAdmin)
admin.site.unregister(Group)
