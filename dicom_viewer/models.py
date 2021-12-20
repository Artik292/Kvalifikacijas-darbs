import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Dicom(models.Model):
    id = models.AutoField(primary_key=True)
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
    textArea = models.TextField(max_length=300,default=" ")
    uploaded_date = models.DateField(auto_now=True)

    def save_dcm_data(self, ds=None):
        self.sop_class = ds.SOPClassUID
        self.patient_name = ds.PatientName.family_name + " " + ds.PatientName.given_name
        self.patient_id = ds.PatientID
        self.modality = ds.Modality
        self.study_date = ds.StudyDate
        self.image_size = str(ds.Rows) + "x" + str(ds.Columns)
        self.pixel_spacing_x = ds.PixelSpacing[0]
        self.pixel_spacing_y = ds.PixelSpacing[1]
        self.slice_location = ds.get('SliceLocation', '(missing)')
        self.save()

    def delete(self, *args, **kwargs):
        if self.dicom_file != "":
            if os.path.isfile(self.dicom_file.path):
                os.remove(self.dicom_file.path)
        if self.file_jpg != "":
            if os.path.isfile(self.file_jpg.path):
                os.remove(self.file_jpg.path)
        super(Dicom, self).delete(*args, **kwargs)