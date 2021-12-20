from django.contrib import admin
from dicom_viewer.models import Dicom

class DicomAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Dicom,DicomAdmin)
