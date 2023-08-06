# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         7/06/23 14:39
# Project:      Zibanu - Django
# Module Name:  groups
# Description:
# ****************************************************************
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from zibanu.django.auth.api.serializers import GroupListSerializer
from zibanu.django.rest_framework.decorators import permission_required
from zibanu.django.rest_framework.viewsets import ModelViewSet


class GroupService(ModelViewSet):
    model = Group
    serializer_class = GroupListSerializer

    @method_decorator(permission_required("group.view_group"))
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @method_decorator(permission_required("group.add_group"))
    def create(self, request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)