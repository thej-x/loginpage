from django.shortcuts import render
from django.shortcuts import HttpResponse,redirect,render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import re

@never_cache
def HomePage(request):
    k = request.user.get_username()
    if request.user.is_authenticated:
        return render(request, 'home.html', {'a': k}) 
    return redirect('login')

@never_cache
def SignupPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if not re.match(r"^[A-Za-z ]+$", fname):
            messages.error(request, "Invalid first name")
            return redirect('signup')

        if not re.match(r"^[A-Za-z ]+$", lname):
            messages.error(request, "Invalid last name")
            return redirect('signup')

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            messages.error(request, "Invalid email")
            return redirect('signup')


        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')
        
        # Create user object
        my_user = User.objects.create_user(username=email, email=email)
        
        # Set first name and last name
        my_user.first_name = fname
        my_user.last_name = lname

        # Set password
        my_user.set_password(pass1)
        
        # Save the user
        my_user.save()
        
        messages.success(request, "Account created successfully. You can now login.")
        return redirect('login')

    return render(request, 'signup.html')
@never_cache
def Loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('email')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"invalid email or password")
            return redirect('login')    
    return render(request,'login.html')

@never_cache
def Logoutpage(request):
    logout(request)
    return redirect('login')

   
    






