from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from account.forms import PatientRegistrationForm, ApplicationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.conf import settings

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
    if request.POST:
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thankYouPage')
        else:
            context['ApplicationForm'] = form
            messages.error(request,'username or password not correct')
    else:
        form = ApplicationForm()
        context['ApplicationForm'] = form
    return render(request, 'main/doctorApplication.html', {'title': 'Doc. Application', 'context' : context}) 
