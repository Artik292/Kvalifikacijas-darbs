from django.contrib import admin
from dicom_viewer.models import Dicom
from account.models import User, Patient, Doctor, DoctorApplication


class DicomAdmin(admin.ModelAdmin):
    list_display = ('id','user','status','uploaded_date','file_jpg')
    readonly_fields=('study_doctor','user','image_size','pixel_spacing_x','pixel_spacing_y','status')

    def delete_queryset(self, request, queryset):

        dicom = queryset.first()
        for dicom in queryset:
            if dicom.study_doctor:
                doctor = Doctor.objects.get(user=dicom.study_doctor)
                doctor.accepted_analysis_count -=1
                doctor.save()
        queryset.delete()

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Dicom,DicomAdmin)
