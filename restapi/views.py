from rest_framework.decorators import api_view
from rest_framework.response import Response
from acl.models import Group, User
from .serializers import *


@api_view(['GET', 'DELETE', 'UPDATE'])
def group_detail(request, pk):
    try:
        group = Group.objects.get(id=pk)
    except Group.DoesNotExist:
        return Response({
            'result': False,
            'data': [],
            'message': "Group doesn't exist.",
        })

    if request.method == "GET":
        serializer = GroupSerializer(group)
        return Response({
            'result': True,
            'data': serializer.data,
            'message': "Successfully extract group information."
            }
        )


@api_view(['GET', 'DELETE', 'UPDATE'])
def user_permission(request, pk):
    try:
        user = User.objects.get(id=pk)
    except Group.DoesNotExist:
        return Response({
            'result': False,
            'data': [],
            'message': "User doesn't exist.",
        })

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response({
            'result': True,
            'data': serializer.data.get("permissions", []),
            'message': "Successfully extract user permission."
            }
        )