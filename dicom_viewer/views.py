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
from .forms import UpdateDicom, UploadDicom, AddMedicalVerdict
from .models import Dicom
from django.core.files import File
from django.core.files.base import ContentFile, File
from .settings import MEDIA_ROOT
from django.views.generic import View
from datetime import datetime, date
from django.core.paginator import Paginator
from account.models import User, Doctor, Patient


import pathlib
import pydicom
import os
import numpy as np
from PIL import Image

@login_required(login_url='home')
@user_passes_test(lambda u: u.is_doctor,login_url='home')
def dataBaseAll(request):
    title = 'Data Base'
    dicoms = Dicom.objects.exclude(status='Finished')
    doctor = Doctor.objects.get(user = request.user)

    # PAGINATOR SETTING
    paginator = Paginator(dicoms, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_pag = page.has_other_pages()

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    return render(request, 'main/dataBase.html',{
        'dicoms':dicoms,
        'title':title,
        'page': page,
        'is_pag': is_pag,
        'next_url': next_url,
        'prev_url': prev_url,
        'doctor':doctor,
    })


@login_required(login_url='home')
@user_passes_test(lambda u: u.is_doctor,login_url='home')
def dataBase(request,slide_id):
    template = "main/database.html"
    title = "Database"
    strId = int(slide_id)
    analysis = Dicom.objects.get(id=slide_id)
    dicom = Dicom.objects.exclude(status='Finished')
    doctor = Doctor.objects.get(user = request.user)

    # PAGINATOR SETTING
    paginator = Paginator(dicom, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_pag = page.has_other_pages()

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    
    context = {
        'dicoms' : dicom,
        'analysis' : analysis,
        'title' : title,
        'id':strId,
        'page': page,
        'is_pag': is_pag,
        'next_url': next_url,
        'prev_url': prev_url,
        'doctor':doctor,
    }
    return render(request,template,context)


@login_required(login_url='home')
@user_passes_test(lambda u: u.is_doctor,login_url='home')
def viewer(request,slide_id):

    dicom = Dicom.objects.get(id = slide_id)
    patient = Patient.objects.get(user=dicom.user)
    user = request.user
    canEdit = False
    checked = False
    template = "main/viewer.html"
    image = dicom .file_jpg.url
    pixel_spacing = [dicom.pixel_spacing_x, dicom.pixel_spacing_y]
    user_name = dicom.patient_name
    # "Jānis Berziņš, 102093-12122, 2021/06-03\n\nSērija:CT, ART 1.25mm\n\nAttēls: 1 / 377\n\nPalielinājums:1.17\n\nW:255 C:127",

    if dicom.study_doctor == user:
        canEdit = True

    if dicom.status == 'Checked':
        checked = True

    if request.method == 'POST':
        form = AddMedicalVerdict(request.POST, instance=dicom)
        if form.is_valid():
            dicom.status = 'Checked'
            form.save()
            return redirect('dataBaseAll')
        else:
            return render(request,template,context = {
                'image': image,
                'pixel_spacing_x': dicom.pixel_spacing_x,
                'pixel_spacing_y': dicom.pixel_spacing_y,
                'user_name': user_name,
                'dicom':dicom,
                'checked':checked,
                'canEdit':canEdit,
                'form':form,
                'patient':patient,
            })

    context = {
        'image': image,
        'pixel_spacing_x': dicom.pixel_spacing_x,
        'pixel_spacing_y': dicom.pixel_spacing_y,
        'user_name': user_name,
        'dicom':dicom,
        'checked':checked,
        'canEdit':canEdit,
        'patient':patient,
    }
    return render(request, template, context=context)   


@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def upload(request):
    error = False
    title = "Upload dicom"
    template = "main/upload.html"
    context = {
        'title':title,
    }
    if request.method == 'POST':
        form = UploadDicom(request.POST, request.FILES)
        if form.is_valid():
            dicom_file = request.FILES.get("dicom_file", None)
            file_name = dicom_file.name
            file_extension = pathlib.Path(file_name).suffix
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
        newid = Dicom.objects.get(id=id)
        newid.delete()
        error = True
        return error
    try:
        final_image = Image.fromarray(scaled_image)
        image_name = str(id) + ".jpg"
        final_image.save(MEDIA_ROOT+'/dicoms/img/'+image_name)
        dicom.file_jpg.save(str(image_name), File(open(os.path.join(MEDIA_ROOT+'/dicoms/img', str(image_name)), "rb"))) 
        dicom.save_dcm_data(ds=ds)
        os.remove(MEDIA_ROOT+'/dicoms/img/'+image_name)
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
    context = {}

    dicom = Dicom.objects.get(id = pk)
    if dicom.status == 'Finished':
        return redirect('archive')

    template_name = 'main/uploadEdit.html'
    title = "Upload info about your analysis"

    form = UpdateDicom(instance=dicom)

    if request.method == 'POST':
        form = UpdateDicom(request.POST, instance=dicom)
        if form.is_valid():
            form.save()
            return redirect('analysis')
        else:
            context['UpdateDicom'] = form
            return render(request, template_name, {
                'title': title,
                'dicom': dicom,
                'file': dicom.dicom_file,
                'name':  dicom.user,
                'context': context,
                'form':form,
            })

    return render(request, template_name, {
        'title': title,
        'dicom': dicom,
        'file': dicom.dicom_file,
        'name':  dicom.user,
        'context': context,
    })

@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def analysis(request):
    title = 'Patient page'
    template_name = 'main/analysis.html'
    dicoms = Dicom.objects.filter(user = request.user).exclude(status='Finished').order_by('-id')
    
    # PAGINATOR SETTING
    paginator = Paginator(dicoms, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_pag = page.has_other_pages()

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    return render(request, template_name, {
        'title':title,
        'dicoms':dicoms,
        'page': page,
        'is_pag': is_pag,
        'next_url': next_url,
        'prev_url': prev_url,
    })

@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def uploadView(request,pk):
    title = 'View your analysis'
    template_name = 'main/uploadView.html'
    dicom = Dicom.objects.get(id=pk)
    link = request.META.get('HTTP_REFERER')
    return render(request, template_name, {
        'title':title,
        'dicom':dicom,
        'link':link,
    })

@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def deleteDicom(request,pk):
    dicom = Dicom.objects.get(id = pk)
    if dicom.study_doctor:
        doctor = Doctor.objects.get(user = dicom.study_doctor)
        doctor.accepted_analysis_count -= 1
        doctor.save()
    dicom.delete()
    return redirect('analysis')

@login_required(login_url='home')
@user_passes_test(lambda u: u.is_doctor,login_url='home')
def accept_view(request,slide_id):
    user = request.user
    doctor = Doctor.objects.get(user = user)

    if doctor.accepted_analysis_count == 5:
        return redirect('dataBaseAll')
    else: 
        doctor.accepted_analysis_count += 1
        dicom = Dicom.objects.get(id=slide_id)
        dicom.study_doctor = user
        dicom.save_status()
        dicom.save()
        doctor.save()
        return redirect('dataBaseAll')

@login_required(login_url='home')
@user_passes_test(lambda u: u.is_doctor,login_url='home')
def decline_view(request,slide_id):
    user = request.user
    dicom = Dicom.objects.get(id=slide_id)
    doctor = Doctor.objects.get(user = user)
    doctor.accepted_analysis_count -= 1
    dicom.study_doctor = None
    dicom.status = 'Uploaded'
    doctor.save()
    dicom.save()
    return redirect('dataBaseAll')

@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def finish(request,slide_id):
    user = request.user
    dicom = Dicom.objects.get(id=slide_id)
    if dicom.user == user:
        if dicom.status == 'Finished':
            return redirect('archive')
        doctor = Doctor.objects.get(user=dicom.study_doctor)
        doctor.accepted_analysis_count -= 1
        dicom.status = 'Finished'
        dicom.save()
        doctor.save()
    return redirect('analysis')

@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def archive(request):
    template_name = 'main/archive.html'
    title = 'Archive'
    dicoms = Dicom.objects.filter(status='Finished')

    # PAGINATOR SETTING
    paginator = Paginator(dicoms, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_pag = page.has_other_pages()

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    return render(request,template_name,{
        'title':title,
        'dicoms':dicoms,
        'page': page,
        'is_pag': is_pag,
        'next_url': next_url,
        'prev_url': prev_url,
    })

@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def declineVerdict(request,slide_id):
    user = request.user
    dicom = Dicom.objects.get(id = slide_id)
    doctor = Doctor.objects.get(user = dicom.study_doctor)
    if dicom.user == user:
        dicom.study_doctor = None
        dicom.status = 'Uploaded'
        dicom.medical_verdict = None
        doctor.accepted_analysis_count -= 1
        dicom.save()
        doctor.save()
    return redirect('analysis')