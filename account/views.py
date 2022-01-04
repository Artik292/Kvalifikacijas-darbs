from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from account.forms import PatientRegistrationForm, ApplicationForm,UpdatePatientInfo
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.conf import settings
from account.models import User, Doctor, Patient

def registration_view(request):
    context = {}
    if request.POST:
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['PatientRegistrationForm'] = form
            return render(request, 'main/register.html',{'title': 'Registration', 'context' : context, 'form' : form})
    else:
        form = PatientRegistrationForm()
        context['PatientRegistrationForm'] = form
    return render(request, 'main/register.html', {'title': 'Registration', 'context' : context}) 


def docAppl_view(request):
    context = {}
    title = 'Doc. Applications'
    if request.POST:
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thankYouPage')
        else:
            context['ApplicationForm'] = form
            return render(request, 'main/doctorApplication.html',{'title': title, 'context' : context, 'form' : form})
    else:
        form = ApplicationForm()
        context['ApplicationForm'] = form
    return render(request, 'main/doctorApplication.html', {'title': title, 'context' : context}) 

def userInfo(request):
    user = request.user
    title = 'Information about user'
    blockLoad = 'main/base.html'
    template = 'main/userInfo.html'
    role = 'patient'
    userInfo = ''

    if user.is_doctor:
        role = 'doctor'
        userInfo = Doctor.objects.get(user=user)
        blockLoad = 'main/forDoctor.html'
    
    context = {}

    if request.POST:
        form = UpdatePatientInfo(request.POST, instance=user)
        if form.is_valid():
            form.save()
        else:
            return render(request,template,context = {
                'role':role,
                'userInfo':userInfo,
                'title':title,
                'blockLoad':blockLoad,
                'form':form,
            })
    else:
        form = UpdatePatientInfo()
        context['UpdatePatientInfo'] = form    
    
    return render(request,template,context = {
        'role':role,
        'userInfo':userInfo,
        'title':title,
        'blockLoad':blockLoad,
    })