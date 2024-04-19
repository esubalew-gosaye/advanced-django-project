from django.shortcuts import render
from acl.include import *
from django.views import View
from resource.forms import ResourceForm
from django.contrib import messages
from resource.models import Resource


class HomePage(View):
    template_name = 'resource/resource.html'
    resource_form = ResourceForm()

    def get(self, request):
        _user = logged_user(request)
        permissions = extract_permissions(_user)
        resources = Resource.objects.all()
        context = {
            'object_list': User.objects.all(),
            'permissions': permissions,
            'resource_form': ResourceForm,
            'resources': resources,
            'logged': {
                'user': User.objects.filter(
                    email=request.session.get('email', '')
                ).first(),
                'email': request.session.get('email', ''),
                'username': request.session.get('username', '')
            }
        }
        return render(request, self.template_name, context)

    def post(self, request):
        forms = ResourceForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            messages.success(request, "Resource saved successfully!")
        return self.get(request)


def home_page(request):
    _user = logged_user(request)
    permissions = extract_permissions(_user)

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
    return render(request, 'resource/resource.html', context)
