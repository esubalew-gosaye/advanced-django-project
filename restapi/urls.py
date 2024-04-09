from django.urls import path
from restapi.views import group_detail, user_permission

urlpatterns = [
    path('v1/group/<str:pk>/', group_detail, name="group-details"),
    path('v1/user/<str:pk>/permissions/', user_permission, name="user-permission"),
]
