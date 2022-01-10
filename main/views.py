from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from account.forms import AccountAuthenticationForm

#function that checks user role and redirects them to the required page
def checkUserForAuth(request, user):
        if user.is_doctor:
            return redirect('dataBaseAll')
        elif user.is_patient:
            return redirect('analysis')
        else:
            return HttpResponseRedirect(reverse('admin:index'))


#home page render with user authentication form
def index(request):
    user = request.user
    if user.is_authenticated:
        return checkUserForAuth(request,user)

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        #check if form is valid
        if form.is_valid():
            #get email and password
            email = request.POST["email"]
            password = request.POST["password"]
            #authenticate user
            user = authenticate(email=email, password=password)

            if user:
                login(request,user)
                return checkUserForAuth(request,user)
    
    else:
        #if form is not valid system displays error on home page
        form = AccountAuthenticationForm()
        messages.error(request,'Email or password not correct')

    return render(request, 'main/index.html',{'form': form})


#this function renders page after doctor has compleated his aplication
def thankYouPage(request):
    return render(request, 'main/thankYouPage.html')


#function that logouts user
def logoutUser(request):
    logout(request)
    return redirect('home')

