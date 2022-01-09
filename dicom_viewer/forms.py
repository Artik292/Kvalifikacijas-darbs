from django import forms
from .models import Dicom
from account.models import User
import os

class UploadDicom(forms.ModelForm):
    class Meta:
        model = Dicom
        fields = ('dicom_file','textArea')
    
    def __init__(self, *args, **kwargs):
        self.file = kwargs.pop('file', None)
        super(UploadDicom, self).__init__(*args, **kwargs)
    
    def clean_dicom_file(self):
        dicom_file = self.cleaned_data.get("dicom_file")
        size = dicom_file.size
        print(size)
        if size > 10485760:
            raise forms.ValidationError("File size is over 10 Mb.")
        return dicom_file
    
class UpdateDicom(forms.ModelForm):
    class Meta:
        model = Dicom
        fields = ('patient_name','study_date','textArea')

class AddMedicalVerdict(forms.ModelForm):
    class Meta:
        model = Dicom
        fields = ('medical_verdict',)
