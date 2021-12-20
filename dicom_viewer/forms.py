from django import forms
from .models import Dicom
from account.models import User

class UploadDicom(forms.ModelForm):
    class Meta:
        model = Dicom
        fields = ('dicom_file',)

