from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.conf import settings

from acl.models import Permission

app_models = apps.get_app_config('acl').get_models()

for models in app_models:
    try:
        admin.site.register(models)
    except AlreadyRegistered:
        pass

# for register a permission to permission model
# my_apps = settings.MY_APPS
# excluded_model = []
#
# for app in my_apps:
#     for models in apps.get_app_config(app).get_models():
#         if models.__name__ not in excluded_model:
#             for allowed_perm in ['view', 'add', 'change', 'delete']:
#                 perm_name = f"{allowed_perm}_{models._meta.verbose_name_plural.replace(' ', '_')}"
#                 perm_description = f'{app} | {models.__name__} | Can {allowed_perm} {models.__name__}'
#
#                 if not Permission.objects.filter(permission=perm_name).exists():
#                     Permission.objects.create(
#                         permission=perm_name,
#                         description=perm_description
#                     )
#         else:
#             for allowed_perm in ['view', 'add', 'change', 'delete']:
#                 try:
#                     perm = Permission.objects.get(
#                         permission=f"{allowed_perm}_{models._meta.verbose_name_plural.replace(' ', '_')}"
#                     )
#                     perm.delete()
#                 except Permission.DoesNotExist:
#                     pass