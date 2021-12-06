from django.shortcuts import render, redirect, reverse
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
# from account.models import Patient

# from account.forms import AccountAuthenticationForm


def index(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect("user")

    # if request.POST:
    #     form = AccountAuthenticationForm(request.POST)
    #     if form.is_valid():
    #         email = request.POST["email"]
    #         password = request.POST["password"]
    #         user = authenticate(email=email, password=password)

    #         if user:
    #             login(request,user)
    #             return redirect(user)
    
    # else:
    #     form = AccountAuthenticationForm()

    return render(request, 'main/index.html')


def thankYouPage(request):
    return render(request, 'main/thankYouPage.html')

def User(request):
    return render(request, 'main/patient.html')



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


def logoutUser(request):
    logout(request)
    return redirect('home')