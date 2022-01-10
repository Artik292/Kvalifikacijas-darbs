from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from account.forms import PatientRegistrationForm, ApplicationForm,UpdatePatientInfo, PatientInfoForm
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.conf import settings
from account.models import User, Doctor, Patient

#this function renders registration template for patients
def registration_view(request):
    context = {}
    if request.POST:
        #get 2 forms
        #form1 is for user creation
        form1 = PatientRegistrationForm(request.POST)
        #form2 is for patient creation
        form2 = PatientInfoForm(request.POST)
        #checks if both forms are valid
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            patient_info = form2.save(commit=False)
            patient_info.user = user
            patient_info.save()
            email = form1.cleaned_data.get("email")
            raw_password = form1.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['PatientRegistrationForm'] = form1
            context['PatientInfoForm'] = form2
            return render(request, 'main/register.html',{'title': 'Registration', 'context' : context, 'form' : form1, 'form2' : form2})
    else:
        form1 = PatientRegistrationForm()
        form2 = PatientInfoForm()
        context['PatientRegistrationForm'] = form1
        context['PatientInfoForm'] = form2
    return render(request, 'main/register.html', {'title': 'Registration', 'context' : context, 'form':form1, 'form2':form2}) 

#this function renders template for doctors aplication
def docAppl_view(request):
    context = {}
    title = 'Doc. Applications'
    if request.POST:
        form = ApplicationForm(request.POST)
        #check form 
        if form.is_valid():
            form.save()
            #if form was completed successfully, unregistrated user will be redirected to thank you page 
            return redirect('thankYouPage')
        else:
            context['ApplicationForm'] = form
            return render(request, 'main/doctorApplication.html',{'title': title, 'context' : context, 'form' : form})
    else:
        form = ApplicationForm()
        context['ApplicationForm'] = form
    return render(request, 'main/doctorApplication.html', {'title': title, 'context' : context}) 

#this function renders user their information
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