from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Dicom(models.Model):
    dicom_file = models.FileField(upload_to='dicoms/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, primary_key = True)

    def _str_(self):
        return self.dicom_file