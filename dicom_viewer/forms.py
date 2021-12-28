from django import forms
from .models import Dicom
from account.models import User

class UploadDicom(forms.ModelForm):
    class Meta:
        model = Dicom
        fields = ('dicom_file','textArea')
    
    def __init__(self, *args, **kwargs):
        self.file = kwargs.pop('file', None)
        super(UploadDicom, self).__init__(*args, **kwargs)
    
class UpdateDicom(forms.ModelForm):
    class Meta:
        model = Dicom
        fields = ('patient_name','study_date','textArea')

class AddMedicalVerdict(forms.ModelForm):
    class Meta:
        model = Dicom
        fields = ('medical_verdict',)
