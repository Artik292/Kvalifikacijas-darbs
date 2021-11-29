from django.shortcuts import render, redirect, reverse
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from account.models import Account

from account.forms import AccountAuthenticationForm

@user_passes_test(lambda u: u.is_doctor,login_url='home')
@login_required(login_url='home')
def dataBase(request):
    return render(request, 'main/dataBase.html')

@user_passes_test(lambda u: u.is_doctor,login_url='home')
@login_required(login_url='home')
def viewer(request):
    return render(request, 'main/viewer.html')