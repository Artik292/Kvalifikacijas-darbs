from django.shortcuts import render, redirect, reverse
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.core.files.storage import FileSystemStorage
from .forms import UploadDicom
from .models import Dicom
from django.core.files import File
from .settings import MEDIA_ROOT
from django.views.generic import View
from datetime import datetime, date


import pydicom
import os
import cv2

@user_passes_test(lambda u: u.is_doctor,login_url='home')
@login_required(login_url='home')
def dataBase(request):
    title = 'Data Base'
    dicoms = Dicom.objects.all()
    return render(request, 'main/dataBase.html',{
        'dicoms':dicoms,
        'title':title
    })

@user_passes_test(lambda u: u.is_doctor,login_url='home')
@login_required(login_url='home')
def viewer(request):
    return render(request, 'main/viewer.html')


def upload(request):
    title = "Upload dicom"
    template = "main/upload.html"
    context = {
        'title':title,
    }
    if request.method == 'POST':
        form = UploadDicom(request.POST, request.FILES)
        if form.is_valid():
            dicom_file = request.FILES.get("dicom_file", None)
            note = form.save(commit=False)
            note.user = request.user
            note.uploaded_date = date.today()
            form.save()
            return from_dcm_to_jpg(note,note.dicom_file,note.id)
    else: 
        form = UploadDicom()
    
    return render(request, template,{
        'title' : title,
        'form' : form
    })

def from_dcm_to_jpg(dicom,dicom_file,id):    
    ds = pydicom.dcmread(os.path.join(dicom_file.path))
    pixel_array_numpy = ds.pixel_array
    image_name = str(id) + ".jpg"
    redirectUrl = 'uploadInfo/'+str(id)
    try:
        cv2.imwrite(os.path.join(MEDIA_ROOT, image_name), pixel_array_numpy)
        dicom.file_jpg.save(str(image_name), File(open(os.path.join(MEDIA_ROOT, str(image_name)), "rb")))            
        dicom.save_dcm_data(ds=ds)
        os.remove(os.path.join(MEDIA_ROOT, image_name))
        newid = Dicom.objects.get(id=id)
        newid.save()
        return redirect(redirectUrl)
    except:
        newid = Dicom.objects.get(id=id)
        newid.delete()


class UploadInfo(View):

    def get(self,request,pk):
        dicom = Dicom.objects.get(id = pk)
        date = dicom.study_date
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]
        new_date = year + '-' + month + '-' + day
        template_name = 'main/uploadInfo.html'
        title = "Upload info about your analysis"
        return render(request, template_name, {
            'title': title,
            'dicom': dicom,
            'file': dicom.dicom_file,
            'name':  dicom.user,
            'date': new_date,
        })


def analysis(request):
    title = 'Patient page'
    template_name = 'main/analysis.html'
    dicoms = Dicom.objects.all()
    return render(request, 'main/analysis.html', {
        'title':title,
        'dicoms':dicoms,
    })


def deleteDicom(request,pk):
    dicom = Dicom.objects.get(id = pk).delete()
    return redirect('analysis')