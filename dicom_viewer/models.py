import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

STATUS = (
    ('None','none'),
    ('Uploaded','uploaded'),
    ('Broken', 'broken'),
)


class Dicom(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS, default='none')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    dicom_file = models.FileField(upload_to='dicoms/dcm', null=True)
    file_jpg = models.FileField(upload_to='dicoms/img', null=True)
    sop_class = models.TextField(null=True)
    patient_name = models.TextField(null=True)
    patient_id = models.TextField(null=True)
    modality = models.TextField(null=True)
    study_date = models.TextField(null=True)
    image_size = models.TextField(null=True)
    pixel_spacing_x = models.TextField(null=True)
    pixel_spacing_y = models.TextField(null=True)
    slice_location = models.TextField(null=True)
    sex = models.TextField(null=True)
    textArea = models.TextField(max_length=300,default=" ")
    uploaded_date = models.DateField(auto_now=True)

    def save_dcm_data(self, ds=None):
        self.patient_id = ds.get('PatientID', 'missing')
        self.patient_name = ds.get('ds.PatientName.family_name' + ' ' + 'ds.PatientName.given_name', 'missing')
        self.sex = ds.get('ds.PatientSex', 'missing')
        self.modality = ds.get('Modality', 'missing')

        date = ds.get('StudyDate', 'missing')
        print(date)
        if date != 'missing':
            year = date[0:4]
            print(year)
            month = date[4:6]
            print(month)
            day = date[6:8]
            print(day)
            new_date = year + '-' + month + '-' + day
        self.study_date = new_date

        self.image_size = ds.get('str(ds.Rows)' + 'x' + 'str(ds.Columns)', 'missing')
        self.patient_name = ds.get('PatientName.family_name' + ' ' + 'ds.PatientName.given_name', 'missing') 
        self.pixel_spacing_x = ds.get('PixelSpacing[0]', 'missing')
        self.pixel_spacing_y = ds.get('PixelSpacing[1]', 'missing')

        if self.image_size == 'missing' or self.pixel_spacing_x == 'missing' or self.pixel_spacing_y == 'missing':
            self.status = 'broken'
        else:
            self.status = 'uploaded'
        self.save()

    def delete(self, *args, **kwargs):
        self.dicom_file.delete()
        self.file_jpg.delete()
        super().delete(*args, **kwargs)