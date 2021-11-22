from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'main/index.html')


# def register(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#         form = CreateUserForm()

#         if request.method == 'POST':
#             form = CreateUserForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 user = form.cleaned_data.get('username')
#                 messages.success(request, 'Account was creater for ' + user)
#                 return redirect('login')

#         context = {'form':form}
#         return render(request, 'main/register.html', context)


# def loginPage(request):

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.info(request, 'username or password is incorrect')

#     context = {}
#     return render(request, 'main/login.html', context)


# def logoutUser(request):
#     logout(request)
#     return redirect('login')