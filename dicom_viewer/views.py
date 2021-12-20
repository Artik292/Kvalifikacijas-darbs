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
    context = {}
    if request.method == 'POST':
        form = UploadDicom(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            form.save()
    else: 
        form = UploadDicom()
    return render(request, 'main/upload.html',{
        'form' : form
    })