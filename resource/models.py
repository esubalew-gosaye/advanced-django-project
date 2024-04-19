from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from acl.models import User


# Create your models here.

# Todo - limit file size - creating a link to access resource - add a permission to resource


class Resource(models.Model):
    name = models.CharField(max_length=120, unique=True,
                            verbose_name=_("Resource name"),
                            error_messages=_("Resource name is required"))
    resource = models.FileField(upload_to='static/resource/',
                                verbose_name=_("Resource"),
                                error_messages=_("Resource field is required"))

    slug_name = models.SlugField(null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        super().save(**kwargs)

    def __str__(self):
        return self.slug_name


class ShareResource(models.Model):
    users = models.ManyToManyField(User, related_name='shares')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='file')
    any_one = models.BooleanField(default=False)
    expire_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateField(auto_created=True)

    def __str__(self):
        return self.resource.name
