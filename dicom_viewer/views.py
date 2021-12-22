from django.db.models import fields
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.core.files.storage import FileSystemStorage
from .forms import UpdateDicom, UploadDicom
from .models import Dicom
from django.core.files import File
from django.core.files.base import ContentFile, File
from .settings import MEDIA_ROOT
from django.views.generic import View
from datetime import datetime, date


import pathlib
import pydicom
import os
import cv2
import numpy as np
from PIL import Image

@user_passes_test(lambda u: u.is_doctor,login_url='home')
@login_required(login_url='home')
def dataBase(request):
    title = 'Data Base'
    dicoms = Dicom.objects.all()
    return render(request, 'main/dataBase.html',{
        'dicoms':dicoms,
        'title':title,
    })


# @user_passes_test(lambda u: u.is_doctor,login_url='home')
# @login_required(login_url='home')
# def viewer(request,id):
#     dicoms = Dicom.objects.get(id = id)
#     return render(request, 'main/viewer.html',{
#         'dicoms':dicoms,
#     })

class Viewer(View):
    def get(self, request, slide_id="0"):
        if slide_id == "":
            image = '../../../static/images/xray.jpg'
            pixel_spacing = [1, 1]
            user_name = "Fedotovs Konstantins, 120278 - 21322"
            data_for_watermark = "Fedotovs Konstantins, 120278 - 21322"
        else:
            dcm = Dicom.objects.filter(id=slide_id)
            if dcm.count():
                dcm = dcm.first()
                image = dcm.file_jpg.url
                pixel_spacing = [dcm.pixel_spacing_x, dcm.pixel_spacing_y]
                user_name = dcm.patient_name
                data_for_watermark = str(user_name) + str(dcm.study_date) #  + "\n\nSērija:CT, ART 1.25mm\n\nAttēls: 1 / 377\n\nPalielinājums:1.17\n\nW:255 C:127"
            else:
                image = '../../../static/images/xray.jpg'
                pixel_spacing = [1, 1]
                user_name = "Fedotovs Konstantins, 120278 - 21322"
                data_for_watermark = "Fedotovs Konstantins, 120278 - 21322"
        template = "main/viewer.html"
        context = {
            'image': image,
            'pixel_spacing_x': pixel_spacing[0],
            'pixel_spacing_y': pixel_spacing[1],
            'user_name': user_name,
            'data_for_watermark': data_for_watermark,
        }
        return render(request, template, context=context)


@user_passes_test(lambda u: u.is_patient,login_url='home')
@login_required(login_url='home')
def upload(request):
    title = "Upload dicom"
    template = "main/upload.html"
    error = False
    context = {
        'title':title,
    }
    if request.method == 'POST':
        form = UploadDicom(request.POST, request.FILES)
        if form.is_valid():
            dicom_file = request.FILES.get("dicom_file", None)
            file_name = dicom_file.name
            file_extension = pathlib.Path(file_name).suffix

            ds = pydicom.dcmread(dicom_file)

            if file_extension == '.dcm' or file_extension == '.DCM':
                note = form.save(commit=False)
                note.user = request.user
                note.uploaded_date = date.today()
                form.save()
                return from_dcm_to_jpg(note,note.dicom_file,note.id)
            else:
                error = True
        else:
            error = True
    else: 
        form = UploadDicom()
    
    return render(request, template,{
        'title' : title,
        'form' : form,
        'error' : error
    })

def from_dcm_to_jpg(dicom,dicom_file,id):    
    ds = pydicom.dcmread(os.path.join(dicom_file.path))
    new_image = ds.pixel_array.astype(float)
    scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
    scaled_image = np.uint8(scaled_image)
    final_image = Image.fromarray(scaled_image)
    image_name = str(id) + ".jpg"
    redirectUrl = 'uploadInfo/'+str(id)
    try:
        final_image.save(MEDIA_ROOT+'/dicoms/img/'+image_name)
        dicom.file_jpg.save(str(image_name), File(open(os.path.join(MEDIA_ROOT+'/dicoms/img', str(image_name)), "rb"))) 
        dicom.save_dcm_data(ds=ds)
        newid = Dicom.objects.get(id=id)
        newid.save()
        return redirect(redirectUrl)
    except:
        newid = Dicom.objects.get(id=id)
        newid.delete()
        error = True
        return redirect('upload'), error

@user_passes_test(lambda u: u.is_patient,login_url='home')
@login_required(login_url='home')
def uploadInfo(request, pk):

    dicom = Dicom.objects.get(id = pk)
    date = dicom.study_date
    template_name = 'main/uploadInfo.html'
    title = "Upload info about your analysis"

    form = UpdateDicom(instance=dicom)

    if request.method == 'POST':
        form = UpdateDicom(request.POST, instance=dicom)
        if form.is_valid():
            form.save()
            return redirect('analysis')

    return render(request, template_name, {
        'title': title,
        'dicom': dicom,
        'file': dicom.dicom_file,
        'name':  dicom.user,
    })

@user_passes_test(lambda u: u.is_patient,login_url='home')
@login_required(login_url='home')
def analysis(request):
    title = 'Patient page'
    template_name = 'main/analysis.html'
    dicoms = Dicom.objects.all().order_by('-id')
    return render(request, 'main/analysis.html', {
        'title':title,
        'dicoms':dicoms,
    })


def deleteDicom(request,pk):
    dicom = Dicom.objects.get(id = pk).delete()
    return redirect('analysis')