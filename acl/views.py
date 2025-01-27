from django.shortcuts import render, redirect, reverse
from acl.models import Group
from django.contrib import messages

from .include import *

from django.utils.translation import gettext_lazy as _

# Create your views here.


def translate(request):

    context = {
        'message': 'trans'
    }
    return render(request, 'acl/translations.html', context)


def home_page(request):
    add_permission_to_db()
    _user = logged_user(request)
    permissions = extract_permissions(_user)

    context = {
        "is_home_page": True,
        'permissions': permissions,
        'logged': {
            'user': User.objects.filter(
                email=request.session.get('email', '')
            ).first(),
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
            _usr = User.objects.filter(email=email, password=password)
            if _usr.exists():
                request.session["username"] = _usr[0].username
                request.session['email'] = _usr[0].email
                messages.success(request, "Welcome, successfully logged in.")
                return redirect(reverse('acl:content-listing') + "?list=users")
            else:
                messages.error(request, "User with this credential doesn't exist!")
        else:
            messages.error(request, "Please Provide both email and password!")
    context = {
        'permissions': permissions,
        'logged': {
            'user': User.objects.filter(
                email=request.session.get('email', '')
            ).first(),
            'email': request.session.get('email', ''),
            'username': request.session.get('username', '')
        }
    }
    return render(request, 'acl/login.html', context)


def content_listing_page(request):
    _user = logged_user(request)
    permissions = extract_permissions(_user)
    groups = Group.objects.all()

    page = request.GET.get('list')

    context = {
        'page': page,
        'users': User.objects.all(),
        'groups': groups,
        'permissions': permissions,
        'logged': {
            'user': User.objects.filter(
                email=request.session.get('email', '')
            ).first(),
            'email': request.session.get('email', ''),
            'username': request.session.get('username', '')
        }
    }
    return render(request, 'acl/list_content.html', context)


def user_creation_page(request):
    _user = logged_user(request)
    permissions = extract_permissions(_user)
    list_groups = Group.objects.all()
    list_permissions = Permission.objects.all()
    group_of_perm = get_grouped_permissions()

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        groups = request.POST.getlist('groups')
        selected_perm = request.POST.getlist('selected_perm')

        new_user = User.objects.create(
            username=username,
            email=email,
            role=role,
        )
        if role == 'user':
            for perm_name in selected_perm:
                new_user.permissions.add(list_permissions.get(permission__contains=perm_name))
        else:
            for perm in list_permissions:
                new_user.permissions.add(perm)
        for group in groups:
            new_user.groups.add(list_groups.get(id=group))
        messages.success(request, "User successfully created.")
        new_user.save()

    context = {
        'permissions': permissions,
        'group_of_perm': group_of_perm,
        'groups': list_groups,
        'logged': {
            'user': User.objects.filter(
                email=request.session.get('email', '')
            ).first(),
            'email': request.session.get('email', ''),
            'username': request.session.get('username', '')
        }
    }
    return render(request, 'acl/user_creation.html', context)


def group_creation_page(request):
    permissions = extract_permissions(logged_user(request))
    group_of_perm = get_grouped_permissions()
    list_permissions = Permission.objects.all()

    if request.method == "POST":
        group_name = request.POST.get('group_name')
        selected_perm = request.POST.getlist('selected_perm')

        new_group = Group.objects.create(
            name=group_name,
        )
        for perm_name in selected_perm:
            new_group.permissions.add(list_permissions.get(permission__contains=perm_name))
        new_group.save()
        messages.success(request, "Group successfully created.")

    context = {
        'permissions': permissions,
        'group_of_perm': group_of_perm,
        'logged': {
            'user': User.objects.filter(
                email=request.session.get('email', '')
            ).first(),
            'email': request.session.get('email', ''),
            'username': request.session.get('username', '')
        }
    }
    return render(request, 'acl/group_creation.html', context)


def user_detail_page(request, pk):
    permissions = extract_permissions(logged_user(request))
    user = User.objects.get(id=pk)

    context = {
        'permissions': permissions,
        'user': user,
        'logged': {
            'user': User.objects.filter(
                email=request.session.get('email', '')
            ).first(),
            'email': request.session.get('email', ''),
            'username': request.session.get('username', '')
        }
    }
    return render(request, 'acl/detail_user.html', context)


def group_detail_page(request, pk):
    permissions = extract_permissions(logged_user(request))
    group = Group.objects.get(id=pk)

    context = {
        'permissions': permissions,
        'group': group,
        'logged': {
            'user': User.objects.filter(
                email=request.session.get('email', '')
            ).first(),
            'email': request.session.get('email', ''),
            'username': request.session.get('username', '')
        }
    }
    return render(request, 'acl/group_detail.html', context)


def group_update_page(request, pk):
    permissions = extract_permissions(logged_user(request))
    group_of_perm = get_grouped_permissions()
    group = Group.objects.get(id=pk)
    list_groups = Group.objects.all()

    if request.method == "POST":
        group_name = request.POST.get('group_name')
        selected_perm = request.POST.getlist('selected_perm')

        group.permissions.clear()
        group.name = group_name
        group.permissions.set(selected_perm)
        messages.info(request, "Group information successfully updated.")
        group.save()

        return redirect(reverse('acl:group-details', args=pk))

    context = {
        'updated_group': group,
        'list_groups': list_groups,
        'group_of_perm': group_of_perm,
        'permissions': permissions,
        'logged': {
            'user': User.objects.filter(
                email=request.session.get('email', '')
            ).first(),
            'email': request.session.get('email', ''),
            'username': request.session.get('username', '')
        }
    }
    return render(request, 'acl/update_group.html', context)


def user_update_page(request, pk):
    group_of_perm = get_grouped_permissions()
    user = User.objects.get(id=pk)
    permissions = extract_permissions(user)
    list_groups = Group.objects.all()

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        groups = request.POST.getlist('groups')
        selected_perm = request.POST.getlist('selected_perm')

        user.permissions.remove()
        user.groups.clear()

        user.username = username
        user.email = email
        user.role = role
        user.groups.set(groups)
        user.permissions.set(selected_perm)

        if role == 'admin':
            user.permissions.set(Permission.objects.all())
        messages.info(request, "User information successfully updated.")
        user.save()

        return redirect(reverse('acl:user-details', args=pk))

    context = {
        'user': user,
        'list_groups': list_groups,
        'group_of_perm': group_of_perm,
        'permissions': permissions,
        'logged': {
            'user': User.objects.filter(
                email=request.session.get('email', '')
            ).first(),
            'email': request.session.get('email', ''),
            'username': request.session.get('username', '')
        }
    }
    return render(request, 'acl/update_user.html', context)


def user_delete(request, pk):
    user = User.objects.get(id=pk)

    # ToDo implement safe delete later
    user.delete()
    return redirect(reverse('acl:content-listing') + 'list=users')


def group_delete(request, pk):
    group = Group.objects.get(id=pk)

    group.delete()
    return redirect(reverse('acl:content-listing') + 'list=groups')


def logout(request):
    _user = logged_user(request)
    messages.info(request, "Successfully logged out.")
    request.session.pop('email', None)
    request.session.pop('username', None)

    return redirect(reverse('acl:login'))
