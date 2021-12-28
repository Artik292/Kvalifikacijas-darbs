import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from account.models import User


sNone = 'None'
Uploaded = 'Uploaded'
Broken = 'Broken'
Inwork = 'In work'
Checked = 'Checked'
Finished = 'Finished'

STATUS = (
    (sNone,'None'),
    (Uploaded,'Uploaded'),
    (Broken, 'Broken'),
    (Inwork, 'In work'),
    (Checked, 'Checked'),
    (Finished, 'Finished'),
)

class Dicom(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='Patient')
    dicom_file = models.FileField(upload_to='dicoms/dcm', null=True)
    file_jpg = models.FileField(upload_to='dicoms/img', null=True, blank=True)
    sop_class = models.TextField(null=True, blank=True)
    patient_name = models.TextField(null=True, blank=True)
    patient_id = models.TextField(null=True, blank=True)
    modality = models.TextField(null=True, blank=True)
    study_date = models.TextField(null=True, blank=True)
    image_size = models.TextField(null=True, blank=True)
    pixel_spacing_x = models.TextField(null=True, blank=True)
    pixel_spacing_y = models.TextField(null=True, blank=True)
    slice_location = models.TextField(null=True, blank=True)
    sex = models.TextField(null=True, blank=True)
    age = models.TextField(null=True,blank=True)
    type = models.TextField(null=True, blank=True)
    textArea = models.TextField(max_length=300,default=" ")
    uploaded_date = models.DateField(auto_now=True, blank=True)
    study_doctor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='Doctor',null=True,blank=True)
    medical_verdict = models.TextField(null=True, blank=True)

    def save_dcm_data(self, ds=None):
        try:
            self.patient_id = ds.get('PatientID', 'missing')
            name = ds.get('PatientName', 'missing')
            name = str(name)
            self.patient_name = name.replace("^"," ")
            self.sex = ds.get('PatientSex', 'missing')
            self.modality = ds.get('Modality', 'missing')
            self.type = ds.get('TransmitCoilName ','missing')
            self.age = ds.get('PatientAge','missing')

            date = ds.get('StudyDate', 'missing')
            if date != 'missing':
                year = date[0:4]
                month = date[4:6]
                day = date[6:8]
                new_date = year + '-' + month + '-' + day
            self.study_date = new_date

            rows = ds.get('Rows','missing')
            columns =  ds.get('Columns','missing')
            if rows!='missing' and columns!='missing':
                imageSize = str(rows) + 'x' + str(columns)
            else:
                imageSize = 'missing'

            self.image_size = imageSize
            pixel_spacing = ds.get('PixelSpacing','missing')
            if pixel_spacing != 'missing':
                self.pixel_spacing_x = pixel_spacing[0]
                self.pixel_spacing_y = pixel_spacing[1]

            if self.image_size == 'missing':
                self.status = 'Broken'
            else:
                self.status = 'Uploaded'
            self.save()
        except:
            pass            

    def delete(self, *args, **kwargs):
        self.dicom_file.delete()
        self.file_jpg.delete()
        super().delete(*args, **kwargs)
    
    def save_status(self):
        self.status = 'In work'
        self.save()
