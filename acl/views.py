from django.shortcuts import render, redirect, reverse
from acl.models import User, Group, TestModel, Permission
from django.utils.translation import gettext as _, get_language, activate

from .include import extract_permissions, logged_user


# Create your views here.


def translate(request):
    # "Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"
    trans = _('Translation')

    context = {
        'message': trans
    }
    return render(request, 'acl/translations.html', context)


def home_page(request):
    _user = logged_user(request)
    permissions = extract_permissions(_user)

    context = {
        "is_home_page": True,
        'permissions': permissions,
        'logged': {
            'email': request.session.get('email', ''),
            'username': request.session.get('username', '')
        }
    }
    return render(request, 'acl/navbar.html', context)


def login(request):
    _user = logged_user(request)
    permissions = extract_permissions(_user)

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get("password")

        if email and password:
            print(email, password)
            _usr = User.objects.filter(email=email, password=password)
            if _usr.exists():
                request.session["username"] = _usr[0].username
                request.session['email'] = _usr[0].email

                return redirect('acl:content-listing')
    context = {
        'permissions': permissions,
        'logged': {
            'email': request.session.get('email', ''),
            'username': request.session.get('username', '')
        }
    }
    return render(request, 'acl/login.html', context)


def content_listing_page(request):
    _user = logged_user(request)
    permissions = extract_permissions(_user)

    context = {
        'users': User.objects.all(),
        'tests': TestModel.objects.all(),
        'permissions': permissions,
        'logged': {
            'email': request.session.get('email', ''),
            'username': request.session.get('username', '')
        }
    }
    return render(request, 'acl/list_content.html', context)


def user_creation_page(request):
    _user = logged_user(request)
    permissions = extract_permissions(_user)
    context = {
        'permissions': permissions,
        'logged': {
            'email': request.session.get('email', ''),
            'username': request.session.get('username', '')
        }
    }
    return render(request, 'acl/user_creation.html', context)


def group_creation_page(request):
    permissions = extract_permissions(logged_user(request))
    group_of_perm = {}
    list_permissions = Permission.objects.all()

    for perm in list_permissions:
        model_name = perm.description.split('|')[1].strip()
        if model_name in group_of_perm:
            group_of_perm[model_name].append(perm)
        else:
            group_of_perm[model_name] = [perm]

    if request.method == "POST":
        group_name = request.POST.get('group_name')
        selected_perm = request.POST.getlist('selected_perm')

        new_group = Group.objects.create(
            name=group_name,
        )
        for perm_name in selected_perm:
            new_group.permissions.add(list_permissions.get(permission__contains=perm_name))
        new_group.save()

    context = {
        'permissions': permissions,
        'group_of_perm': group_of_perm,
        'logged': {
            'email': request.session.get('email', ''),
            'username': request.session.get('username', '')
        }
    }
    return render(request, 'acl/group_creation.html', context)


def logout(request):
    _user = logged_user(request)

    request.session.pop('email', None)
    request.session.pop('username', None)

    return redirect(reverse('acl:login'))
