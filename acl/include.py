from django.conf import settings
from acl.models import Permission, User
from django.apps import apps

from django.db.models.signals import post_migrate
from django.dispatch import receiver


def logged_user(request):
    _user = User.objects.filter(email=request.session.get('email', ''))
    return _user


def extract_permissions(user):
    permissions = []
    if user.exists():
        user = user[0]

        for perm in user.permissions.select_related():
            permissions.append(perm.permission)

        for group in user.groups.select_related():
            for perm in group.permissions.select_related():
                permissions.append(perm.permission)

        print(permissions)
    return permissions


@receiver(post_migrate)
def add_permission_to_db(**kwargs):
    # for register a permission to permission model
    my_apps = settings.MY_APPS
    excluded_model = []

    for app in my_apps:
        for models in apps.get_app_config(app).get_models():
            if models.__name__ not in excluded_model:
                for allowed_perm in ['view', 'add', 'change', 'delete']:
                    perm_name = f"{allowed_perm}_{models._meta.verbose_name_plural.replace(' ', '_')}"
                    perm_description = f'{app} | {models.__name__} | Can {allowed_perm} {models.__name__}'

                    if not Permission.objects.filter(permission=perm_name).exists():
                        Permission.objects.create(
                            permission=perm_name,
                            description=perm_description
                        )
            else:
                for allowed_perm in ['view', 'add', 'change', 'delete']:
                    try:
                        perm = Permission.objects.get(
                            permission=f"{allowed_perm}_{models._meta.verbose_name_plural.replace(' ', '_')}"
                        )
                        perm.delete()
                    except Permission.DoesNotExist:
                        pass
