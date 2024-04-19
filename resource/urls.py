from django.urls import path
from resource.views import *

app_name = "resource"
urlpatterns = [
    path("", HomePage.as_view(), name="resource-homepage")
]