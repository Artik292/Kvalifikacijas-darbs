from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from account.forms import AccountAuthenticationForm


def checkUserForAuth(request, user):
        if user.is_doctor:
            return redirect('dataBaseAll')
        elif user.is_patient:
            return redirect('analysis')
        else:
            return HttpResponseRedirect(reverse('admin:index'))


def index(request):
    user = request.user
    if user.is_authenticated:
        return checkUserForAuth(request,user)

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)

            if user:
                login(request,user)
                return checkUserForAuth(request,user)
    
    else:
        form = AccountAuthenticationForm()
        messages.error(request,'Email or password not correct')

    return render(request, 'main/index.html',{'form': form})


def thankYouPage(request):
    return render(request, 'main/thankYouPage.html')


def logoutUser(request):
    logout(request)
    return redirect('home')

