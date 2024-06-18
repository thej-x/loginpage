from django.shortcuts import render
from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
import re
from app1.models import Users
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
@never_cache
def homePage(request):
    k = request.user.get_username()
    if request.user.is_authenticated:
        return render(request, 'home.html', {'a': k}) 
    return redirect('login')

@never_cache
def signupPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if ' ' in uname :
            messages.error(request, "Username cannot contain spaces")
            return redirect('signup')

        if ' ' in email:
            messages.error(request, "Email cannot contain spaces")
            return redirect('signup')
        
        if not re.match(r"^[A-Za-z ]+$", uname):
            messages.error(request, "Invalid username name")
            return redirect('signup')
        
        elif User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exsist")
            return redirect('signup')
        
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            messages.error(request, "Invalid email")
            return redirect('signup')
        
        elif User.objects.filter(email=email).exists():
            messages.error(request, "email already exsist")
            return redirect('signup')   
             
        if pass1 == None and pass2==None:
            messages.error(request, "Fill password fileds")
            return redirect('signup')
        
        if len(pass1) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return redirect('signup')
        
        if not any(char.isupper() for char in pass1):
            messages.error(request, "Password must contain at least one uppercase letter")
            return redirect('signup')

        if pass1 != pass2 :
            messages.error(request, "Passwords do not match")
            return redirect('signup')
        
        # Create user object
        my_user = User.objects.create_user(username=uname, email=email)
        
        # Set first name and last name
        my_user.user_name = uname

        # Set password
        my_user.set_password(pass1)
        
        # Save the user
        my_user.save()
        
        messages.success(request, "Account created successfully. You can now login.")
        return redirect('login')

    return render(request,'signup.html')

@never_cache
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        uname=request.POST.get('username')
        print(uname)
        pass1=request.POST.get('password')
        print(pass1)
        user=authenticate(request,username=uname,password=pass1)
        print(user,'Workimg')
        if user is not None:
            ('not none   ')
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"invalid username or password")
            return redirect('login')    
    return render(request,'login.html')

@never_cache
def logoutpage(request):
    logout(request)
    return redirect('login')

@never_cache
def adminpage(request):
    context = {} 
    
    if request.user.is_authenticated:
        usr = User.objects.exclude(is_superuser=True)
        
        if 'search' in request.GET:
            search = request.GET['search']
            usr = usr.filter(username__icontains=search)
        
        context = {
            'usr': usr
        }
    else:
        return redirect('login')
    
    return render(request, 'admin.html', context)
   
def add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  
        
        

        # Input validation
        if ' ' in username:
            messages.error(request, "Username cannot contain spaces")
            return redirect('add')

        if not re.match(r"^[A-Za-z ]+$", username):
            messages.error(request, "Invalid username format")
            return redirect('add')
        
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exsist")
            return redirect('add')        

        if ' ' in email:
            messages.error(request, "Email cannot contain spaces")
            return redirect('add')

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            messages.error(request, "Invalid email format")
            return redirect('add')
        
        elif User.objects.filter(email=email).exists():
            messages.error(request, "email already exsist")
            return redirect('add')
        

        # Create user
        try:
            usr = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "User created successfully")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('add')
        
        


    return redirect('adminpage')

def edit(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Input validation
        if ' ' in username:
            messages.error(request, "Username cannot contain spaces")
            return redirect('edit')

        if not re.match(r"^[A-Za-z ]+$", username):
            messages.error(request, "Invalid username format")
            return redirect('edit')
        
        user_id = request.POST.get('user_id')
        user = User.objects.get(pk=user_id)

        if user.username != username and User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('edit')

        if ' ' in email:
            messages.error(request, "Email cannot contain spaces")
            return redirect('edit')

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            messages.error(request, "Invalid email format")
            return redirect('edit')
        
        if user.email != email and User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('edit')

        # Update user
        try:
            # Update user fields
            user.username = username
            user.email = email
            user.save()
            messages.success(request, "User updated successfully")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('edit')
    
    
    usr = User.objects.exclude(is_superuser=True)
    context = {
        
        'usr': usr,
        
    }
    
    

    return render(request,'admin.html',context)

def update(request, id):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Input validation
        if ' ' in username:
            messages.error(request, "Username cannot contain spaces")
            return redirect('edit')

        if not re.match(r"^[A-Za-z ]+$", username):
            messages.error(request, "Invalid username format")
            return redirect('edit')
        
        user = User.objects.get(pk=id)

        if user.username != username and User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('edit')

        if ' ' in email:
            messages.error(request, "Email cannot contain spaces")
            return redirect('edit')

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            messages.error(request, "Invalid email format")
            return redirect('edit')
        
        if user.email != email and User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('edit')

        # Update user
        try:
            # Update user fields
            user.username = username
            user.email = email
            user.save()
            messages.success(request, "User updated successfully")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('adminpage')

    return render(request, 'admin.html')

2 
def delete(request,id):
        usr = User.objects.filter(id=id)
        usr.delete()
        context={
            'usr':usr,
        }
        return redirect('adminpage')
