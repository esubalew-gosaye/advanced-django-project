from django.db import models


class RestModel(models.Model):
    api_version = models.CharField(max_length=4, default='v1')
    manager = models.CharField(max_length=5)
