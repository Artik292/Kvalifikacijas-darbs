from django import forms
from .models import Dicom
from account.models import User
import os

#form to upload dicom 
class UploadDicom(forms.ModelForm):
    class Meta:
        model = Dicom
        fields = ('dicom_file','textArea')
    
    def __init__(self, *args, **kwargs):
        self.file = kwargs.pop('file', None)
        super(UploadDicom, self).__init__(*args, **kwargs)
    
    #function that checks dicoms size
    def clean_dicom_file(self):
        dicom_file = self.cleaned_data.get("dicom_file")
        size = dicom_file.size
        if size > 10485760:
            #if size more than 10 mb returns error
            raise forms.ValidationError("File size is over 10 Mb.")
        return dicom_file

#form to update dicom  
class UpdateDicom(forms.ModelForm):
    class Meta:
        model = Dicom
        fields = ('patient_name','study_date','textArea')

#form to add medical verdict
class AddMedicalVerdict(forms.ModelForm):
    class Meta:
        model = Dicom
        fields = ('medical_verdict',)
