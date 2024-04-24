from django.shortcuts import render
from acl.include import *
from django.views import View
from resource.forms import ResourceForm
from django.contrib import messages
from resource.models import *


class HomePage(View):
    template_name = 'resource/resource.html'
    resource_form = ResourceForm()

    def get(self, request):
        _user = logged_user(request)
        permissions = extract_permissions(_user)
        resources = Resource.objects.all()
        users = User.objects.all()

        context = {
            'object_list': User.objects.all(),
            'permissions': permissions,
            'resource_form': ResourceForm,
            'resources': resources,
            'users': users,
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
        res_id = request.POST.get('resource_id')
        any_one = request.POST.get('any_one')
        users = request.POST.getlist('users')
        expire = request.POST.get('expire_date')

        _res = Resource.objects.get(id=res_id)
        _share = ShareResource.objects.filter(resource=_res)
        if _share.exists():
            _share = _share.first()
            _share.any_one = True if any_one == 'on' else False
            _share.expire_date = None if expire == "" else expire
            _share.users.set(users)
            _share.save()
        else:
            created = ShareResource.objects.update_or_create(
                any_one=True if any_one == 'on' else False,
                resource=_res,
                expire_date=None if expire == "" else expire
            )
            created.users.set(users)

        messages.success(request, "Resource sharing info saved.")

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
