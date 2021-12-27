from django.db.models import fields
from django.forms.widgets import TimeInput
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

@login_required(login_url='home')
@user_passes_test(lambda u: u.is_doctor,login_url='home')
def dataBaseAll(request):
    title = 'Data Base'
    dicoms = Dicom.objects.all()
    return render(request, 'main/dataBase.html',{
        'dicoms':dicoms,
        'title':title,
    })




def dataBase(request,slide_id):
    template = "main/database.html"
    title = "Database"
    strId = int(slide_id)
    analysis = Dicom.objects.get(id=slide_id)
    dicom = Dicom.objects.all()
    
    context = {
        'dicoms' : dicom,
        'analysis' : analysis,
        'title' : title,
        'id':strId
    }
    return render(request,template,context)





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
            'dicom':dcm,
        }
        return render(request, template, context=context)


@user_passes_test(lambda u: u.is_patient,login_url='home')
@login_required(login_url='home')
def upload(request):
    error = False
    title = "Upload dicom"
    template = "main/upload.html"
    context = {
        'title':title,
    }
    if request.method == 'POST':
        dicom_file = request.FILES.get("dicom_file", None)
        file_name = dicom_file.name
        file_extension = pathlib.Path(file_name).suffix
        form = UploadDicom(request.POST, request.FILES)
        if form.is_valid():
            if file_extension == '.dcm' or file_extension == '.DCM':
                note = form.save(commit=False)
                note.user = request.user
                note.uploaded_date = date.today()
                form.save()
                error = from_dcm_to_jpg(note,note.dicom_file,note.id,error)
                if error:
                    return render(request, template,{
                        'title' : title,
                        'form' : form,
                        'error' : error
                    })
                else:
                    redirectUrl = 'uploadEdit/'+str(note.id)
                    print(redirectUrl)
                    return redirect(redirectUrl)
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

def from_dcm_to_jpg(dicom,dicom_file,id,error):    
    ds = pydicom.dcmread(os.path.join(dicom_file.path))
    new_image = ds.pixel_array
    scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
    scaled_image = np.uint8(scaled_image)
    if scaled_image.ndim > 2:
        error = True
        return error
    try:
        final_image = Image.fromarray(scaled_image)
        image_name = str(id) + ".jpg"
        final_image.save(MEDIA_ROOT+'/dicoms/img/'+image_name)
        dicom.file_jpg.save(str(image_name), File(open(os.path.join(MEDIA_ROOT+'/dicoms/img', str(image_name)), "rb"))) 
        dicom.save_dcm_data(ds=ds)
        newid = Dicom.objects.get(id=id)
        newid.save()
        error = False
        return error
    except:
        newid = Dicom.objects.get(id=id)
        newid.delete()
        error = True
        return error

@user_passes_test(lambda u: u.is_patient,login_url='home')
@login_required(login_url='home')
def uploadEdit(request, pk):

    dicom = Dicom.objects.get(id = pk)
    date = dicom.study_date
    template_name = 'main/uploadEdit.html'
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
    return render(request, template_name, {
        'title':title,
        'dicoms':dicoms,
    })

def uploadView(request,pk):
    title = 'View your analysis'
    template_name = 'main/uploadView.html'
    dicom = Dicom.objects.get(id=pk)
    return render(request, template_name, {
        'title':title,
        'dicom':dicom,
    })


def deleteDicom(request,pk):
    Dicom.objects.get(id = pk).delete()
    return redirect('analysis')


def accept_view(requeset,slide_id):
    user = requeset.user
    dicom = Dicom.objects.get(id=slide_id)
    dicom.study_doctor = user
    dicom.save_status()
    dicom.save()
    return redirect('dataBaseAll')

def decline_view(request,slide_id):
    dicom = Dicom.objects.get(id=slide_id)
    dicom.study_doctor = None
    dicom.status = 'Uploaded'
    dicom.save()
    return redirect('dataBaseAll')