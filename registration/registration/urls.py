"""
URL configuration for registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.signupPage,name='signup'),
    path('login/',views.loginpage,name='login'),
    path('home/',views.homePage,name='home'),
    path('logout/',views.logoutpage,name='logout'),
    path('adminpage/',views.adminpage,name='adminpage'),
    path('add/',views.add,name='add'),
    path('edit/',views.edit,name='edit'),
    path('update/<str:id>',views.update,name='update'),
    path('delete/<str:id>',views.delete,name='delete'),
    
] #last commit
