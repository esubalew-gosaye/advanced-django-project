from django.shortcuts import render
from django.contrib import messages
# Create your views here.


def home_page(request):
    messages.success(request, "This is success message")
    messages.error(request, "This is error message that added by the user")
    is_home_page = True
    context = {
        "is_home_page": is_home_page
    }
    return render(request, 'acl/navbar.html', context)

def login(request):
    context = {

    }
    return render(request, 'acl/login.html')

def user_creation_page(request):
    context = {

    }
    return render(request, 'acl/user_creation.html', context)

def group_creation_page(request):
    context = {

    }
    return render(request, 'acl/group_creation.html', context)

def logout(request):
    context = {

    }
    return render(request, 'acl/login.html')