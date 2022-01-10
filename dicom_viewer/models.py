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
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='Patient',on_delete=models.CASCADE)
    dicom_file = models.FileField(upload_to='dicoms/dcm', null=True)
    file_jpg = models.FileField(upload_to='dicoms/img', null=True, blank=True)
    patient_name = models.TextField(null=True)
    patient_id = models.TextField(null=True, blank=True)
    modality = models.TextField(null=True, blank=True)
    study_date = models.TextField(null=True)
    image_size = models.TextField(null=True, blank=True)
    pixel_spacing_x = models.TextField(null=True, blank=True)
    pixel_spacing_y = models.TextField(null=True, blank=True)
    sex = models.TextField(null=True, blank=True)
    age = models.TextField(null=True,blank=True)
    textArea = models.TextField(max_length=300,default=" ")
    uploaded_date = models.DateField(auto_now=True, blank=True)
    study_doctor = models.ForeignKey(User,related_name='Doctor',null=True,blank=True,on_delete=models.SET_NULL)
    medical_verdict = models.TextField(null=True)

    # function that reads dicom file and saves information to the database fields
    def save_dcm_data(self, ds=None):
        try:
            print(ds)
            # get information about patient from file
            self.patient_id = ds.get('PatientID', 'missing')
            name = ds.get('PatientName', 'missing')
            name = str(name)
            self.patient_name = name.replace("^"," ")
            self.sex = ds.get('PatientSex', 'missing')
            self.modality = ds.get('Modality', 'missing')
            self.type = ds.get('TransmitCoilName ','missing')
            self.age = ds.get('PatientAge','missing')
            # get date and convert it to the new format for html input type date
            date = ds.get('StudyDate', 'missing')
            if date != 'missing':
                year = date[0:4]
                month = date[4:6]
                day = date[6:8]
                new_date = year + '-' + month + '-' + day
            self.study_date = new_date
            # get image resolution
            rows = ds.get('Rows','missing')
            columns =  ds.get('Columns','missing')
            if rows!='missing' and columns!='missing':
                imageSize = str(rows) + 'x' + str(columns)
            else:
                imageSize = 'missing'
            self.image_size = imageSize
            # get pixel spacing 
            pixel_spacing = ds.get('PixelSpacing','missing')
            if pixel_spacing != 'missing':
                self.pixel_spacing_x = pixel_spacing[0]
                self.pixel_spacing_y = pixel_spacing[1]

            # if file doesnt have image size or pixel spacing status is broken 
            if self.image_size == 'missing' or pixel_spacing =='missing':
                self.status = 'Broken'
            else:
                # if everything is ok then status is uploaded
                self.status = 'Uploaded'
            self.save()
        except:
            pass            
    
    #when user delets dicom analysis data from server deletes too
    def delete(self, *args, **kwargs):
        self.dicom_file.delete()
        self.file_jpg.delete()
        super().delete(*args, **kwargs)

