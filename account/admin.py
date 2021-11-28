from django.contrib import admin
from account.models import Account
from account.models import Doctor
from account.forms import RegistrationForm


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('username','date_joined')
    list_filter = ('date_joined',)
    change_list_template = 'admin/account/accountChangeDoctor.html'

    actions = ['Approve']

    def Approve(self,request,queryset):
        # queryset.delete()
        user = queryset.first()
        for user in queryset:
            newUser = Account.objects.create(first_name=user.first_name,last_name=user.last_name,email=user.email,username=user.username,pers_code=user.pers_code,password=user.password,is_doctor=user.is_doctor)
            newUser.save()
        queryset.delete()
        


admin.site.site_header = "Admin Dashboard"
admin.site.register(Account)
admin.site.register(Doctor, DoctorAdmin)
