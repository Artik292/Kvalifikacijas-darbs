from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from .forms import UpdateDicom, UploadDicom, AddMedicalVerdict
from .models import Dicom
from django.core.files import File
from django.core.files.base import File
from .settings import MEDIA_ROOT
from datetime import date
from django.core.paginator import Paginator
from account.models import Doctor, Patient
import pathlib
import pydicom
import os
import numpy as np
from PIL import Image

#this function renders database template with all analyzes
@login_required(login_url='home')
@user_passes_test(lambda u: u.is_doctor,login_url='home')
def dataBaseAll(request):
    checkDevice(request)
    title = 'Data Base'
    #get all analyzes except for those with status is "Finished"
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

#this function renders database template with all analyzes and specific analysis that doctor has selected before
@login_required(login_url='home')
@user_passes_test(lambda u: u.is_doctor,login_url='home')
def dataBase(request,slide_id):
    checkDevice(request)
    template = "main/database.html"
    title = "Database"
    strId = int(slide_id)
    #get specific analysis
    analysis = Dicom.objects.get(id=slide_id)
    #get all analyzes except for those with status is "Finished"
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


#this function renders viewer for dicom research for doctor
@login_required(login_url='home')
@user_passes_test(lambda u: u.is_doctor,login_url='home')
def viewer(request,slide_id):
    checkDevice(request)
    #get dicom info
    dicom = Dicom.objects.get(id = slide_id)
    #get patient info
    patient = Patient.objects.get(user=dicom.user)
    user = request.user
    canEdit = False
    template = "main/viewer.html"
    image = dicom .file_jpg.url
    user_name = dicom.patient_name

    #check if doctor has accepted this dicom. If he is, he can view dicom and write medical reports
    if dicom.study_doctor == user:
        canEdit = True

    # if doctor wants to upload medical verdict about dicom
    if request.method == 'POST':
        form = AddMedicalVerdict(request.POST, instance=dicom)
        #check if form is valid and status is in work. Otherwise doctor couldnt upload his medical verdict
        if form.is_valid() and dicom.status == 'In work':
            #if everythings okay, dicom status changes to Checked
            dicom.status = 'Checked'
            #form saves
            form.save()
            #system redirects doctor to all analyzes
            return redirect('dataBaseAll')
        else:
            return render(request,template,context = {
                'image': image,
                'pixel_spacing_x': dicom.pixel_spacing_x,
                'pixel_spacing_y': dicom.pixel_spacing_y,
                'user_name': user_name,
                'dicom':dicom,
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
        'canEdit':canEdit,
        'patient':patient,
    }
    return render(request, template, context=context)   

# View where user can uplaod dicom 
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
        # Check if form  is valid
        if form.is_valid():
            # get uploaded file extension
            dicom_file = request.FILES.get("dicom_file", None)
            file_name = dicom_file.name
            file_extension = pathlib.Path(file_name).suffix
            # check if uploaded file is .dcm format
            if file_extension == '.dcm' or file_extension == '.DCM':                    
                note = form.save(commit=False)
                note.user = request.user
                note.uploaded_date = date.today()
                form.save()
                # call function that returns true if could not create an image from file, or false if could
                error = from_dcm_to_jpg(note,note.dicom_file,note.id,error)
                # if error is true system shows error message
                if error:
                    return render(request, template,{
                        'title' : title,
                        'form' : form,
                        'error' : error
                    })
                else:
                    # if system made image from file user will be redirected to the page where he could edit uploaded file
                    redirectUrl = 'uploadEdit/'+str(note.id)
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

# function that creates image from dicom file and returns errors status (true or false)
def from_dcm_to_jpg(dicom,dicom_file,id,error):
    try:
        # read file with pydicom 
        ds = pydicom.dcmread(os.path.join(dicom_file.path))
        # get pixel array
        new_image = ds.pixel_array
        scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
        scaled_image = np.uint8(scaled_image)
        # if array has more than two dimensions return false
        if scaled_image.ndim > 2:
            newid = Dicom.objects.get(id=id)
            newid.delete()
            error = True
            return error
        # create image from pixel array 
        final_image = Image.fromarray(scaled_image)
        image_name = str(id) + ".jpg"
        # save temporary image 
        final_image.save(MEDIA_ROOT+'/dicoms/img/'+image_name)
        # save new image 
        dicom.file_jpg.save(str(image_name), File(open(os.path.join(MEDIA_ROOT+'/dicoms/img', str(image_name)), "rb"))) 
        # save informatition from dicom file to the system database 
        dicom.save_dcm_data(ds=ds)
        #remove temporary image
        os.remove(MEDIA_ROOT+'/dicoms/img/'+image_name)
        newid = Dicom.objects.get(id=id)
        newid.save()
        error = False
        return error
    except:
        # return false if system cannot create image or save data
        newid = Dicom.objects.get(id=id)
        newid.delete()
        error = True
        return error

#this function renders edit dicom template for patient
@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def uploadEdit(request, pk):
    context = {}
    user = request.user
    dicom = Dicom.objects.get(id = pk)
    #user cannot change finished dicoms. So if he manually enters link in url, system will redirect him to archive page
    if dicom.status == 'Finished':
        return redirect('archive')
    #if patient is not the one who uploaded this dicom, system will redirect him to analysis page
    if dicom.user != user:
        return redirect('analysis')
    template_name = 'main/uploadEdit.html'
    title = "Upload info about your analysis"

    form = UpdateDicom(instance=dicom)

    #if patient uploads the form with dicom data
    if request.method == 'POST':
        form = UpdateDicom(request.POST, instance=dicom)
        #check if form is valid
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

#this fucntion renders to patient his all uploaded analyzes on one page
@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def analysis(request):
    title = 'Patient page'
    template_name = 'main/analysis.html'
    #get all patients analyzes exept finished ones and order them from fresh to old  
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

#this function renders page where patient can view his uploaded dicom
@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def uploadView(request,pk):
    user = request.user
    title = 'View your analysis'
    template_name = 'main/uploadView.html'
    dicom = Dicom.objects.get(id=pk)
    #if patient is really the one who uploaded this dicom, them system renders it
    if dicom.user == user:

        return render(request, template_name, {
            'title':title,
            'dicom':dicom,
        })
    else:
        #otherwise redirects to analysis page
        return redirect('analysis')

#this function deletes dicoms from database
@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def deleteDicom(request,pk):
    dicom = Dicom.objects.get(id = pk)
    user = request.user
    #dicom could be deleted only by his owner. System checks dicoms patient. If fails, patient is redirected to analysis page
    if dicom.user != user:
        return redirect('analysis')
    #if dicom is not finished and has study doctor then study doctors accepted analyzes count becomes one less
    if dicom.study_doctor and dicom.status != 'Finished':
        doctor = Doctor.objects.get(user = dicom.study_doctor)
        doctor.accepted_analysis_count -= 1
        doctor.save()
    #delete dicom
    dicom.delete()
    return redirect('analysis')

#this function allows to accept dicom for doctors
@login_required(login_url='home')
@user_passes_test(lambda u: u.is_doctor,login_url='home')
def accept_view(request,slide_id):
    checkDevice(request)
    user = request.user
    doctor = Doctor.objects.get(user = user)
    dicom = Dicom.objects.get(id=slide_id)

    #doctor cant have more than 5 accepted analyzes at once. Also if dicom has already have study doctor or its status if Uplaoded, doctor cant accept this dicom 
    if doctor.accepted_analysis_count == 5 or dicom.study_doctor or dicom.status != 'Uploaded':
        return redirect('dataBaseAll')
    else: 
        #otherwise doctors accopted analyzes count becomes one more
        doctor.accepted_analysis_count += 1
        dicom.study_doctor = user
        #dicom status becomes In work
        dicom.status = 'In work'
        dicom.save()
        doctor.save()
        return redirect('dataBaseAll')

#this function allows decline dicoms for doctor
@login_required(login_url='home')
@user_passes_test(lambda u: u.is_doctor,login_url='home')
def decline_view(request,slide_id):
    checkDevice(request)
    user = request.user
    dicom = Dicom.objects.get(id=slide_id)
    #doctor can decline dicom if its status is In work and he is the study doctor
    if dicom.status == 'In work' and dicom.study_doctor == user:
        doctor = Doctor.objects.get(user = user)
        # doctors accepted analyzes count becomes one less
        doctor.accepted_analysis_count -= 1
        dicom.study_doctor = None
        #dicoms status changes to Uploaded
        dicom.status = 'Uploaded'
        doctor.save()
        dicom.save()
    return redirect('dataBaseAll')

#this function allows patient to finish the dicoms research
@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def finish(request,slide_id):
    user = request.user
    dicom = Dicom.objects.get(id=slide_id)
    #if patient is really the owner of this dicom and dicoms status is Checked
    if dicom.user == user and dicom.status == 'Checked':
        doctor = Doctor.objects.get(user=dicom.study_doctor)
        # doctors accepted analyzes count becomes one less
        doctor.accepted_analysis_count -= 1
        #dicoms status changes to Finished
        dicom.status = 'Finished'
        dicom.save()
        doctor.save()
        return redirect('archive')
    return redirect('analysis')

#this function renders archive with all patients finished analyzes
@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def archive(request):
    template_name = 'main/archive.html'
    title = 'Archive'
    user = request.user
    #get all patients analyzes with status Finished
    dicoms = Dicom.objects.filter(status='Finished',user=user)

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

#this function allows patient to decline medical verdict from doctor
@login_required(login_url='home')
@user_passes_test(lambda u: u.is_patient,login_url='home')
def declineVerdict(request,slide_id):
    user = request.user
    dicom = Dicom.objects.get(id = slide_id)
    doctor = Doctor.objects.get(user = dicom.study_doctor)
    #check if patient is the owner of this dicom and dicom status is Chcecked
    if dicom.user == user and dicom.status=="Checked":
        dicom.study_doctor = None
        #change dicom status to uploaded
        dicom.status = 'Uploaded'
        dicom.medical_verdict = None
        doctor.accepted_analysis_count -= 1
        dicom.save()
        doctor.save()
    return redirect('analysis')


def checkDevice(request):
    if not request.user_agent.is_pc:
        return redirect('is-not-computer')
    else:
        return

def is_not_computer(request):
    return render(request,'main/isMobile.html')