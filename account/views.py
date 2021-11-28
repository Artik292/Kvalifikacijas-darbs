from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from account.forms import RegistrationForm, ApplicationForm
from django.views.decorators.csrf import csrf_protect

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'main/register.html', {'title': 'Registration', 'context' : context}) 


def docAppl_view(request):
    context = {}
    if request.POST:
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thankYouPage')
        else:
            context['application_form'] = form
    else:
        form = ApplicationForm()
        context['application_form'] = form
    return render(request, 'main/doctorApplication.html', {'title': 'Doc. Application', 'context' : context}) 
