from django.contrib import admin
from dicom_viewer.models import Dicom
from account.models import User, Patient, Doctor, DoctorApplication


class DicomAdmin(admin.ModelAdmin):
    list_display = ('id','user')
    readonly_fields=('study_doctor','user')

    def delete_queryset(self, request, queryset):

        dicom = queryset.first()
        for dicom in queryset:
            if dicom.study_doctor:
                doctor = Doctor.objects.get(user=dicom.study_doctor)
                doctor.accepted_analysis_count -=1
                doctor.save()
        queryset.delete()

admin.site.register(Dicom,DicomAdmin)
