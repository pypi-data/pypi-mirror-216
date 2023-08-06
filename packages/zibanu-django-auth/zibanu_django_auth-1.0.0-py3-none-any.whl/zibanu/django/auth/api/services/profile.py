# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         19/06/23 14:29
# Project:      Zibanu - Django
# Module Name:  profile
# Description:
# ****************************************************************
from rest_framework import status
from rest_framework.response import Response
from zibanu.django.auth.api.serializers import ProfileSerializer
from zibanu.django.auth.models import UserProfile
from zibanu.django.rest_framework.exceptions import ValidationError, APIException
from zibanu.django.rest_framework.viewsets import ModelViewSet
from zibanu.django.utils.error_messages import ErrorMessages
from zibanu.django.utils.user import get_user

class ProfileService(ModelViewSet):
    model = UserProfile
    serializer_class = ProfileSerializer

    def update(self, request, *args, **kwargs) -> Response:
        """
        Override method to update a profile from an authenticated user
        :param request: request object from HTTP
        :param args: tuple args
        :param kwargs: dict kwargs
        :return: response with status
        """
        try:
            if request.data is not None:
                user = get_user(request.user)
                if hasattr(user, "profile"):
                    user.profile.set(fields=request.data)
                else:
                    raise ValidationError(ErrorMessages.NOT_FOUND, "user_profile_not_found")
            else:
                raise ValidationError(ErrorMessages.DATA_REQUEST_NOT_FOUND, "data_request_error")
        except ValidationError as exc:
            raise APIException(msg=exc.detail[0], error=exc.detail[0].code, http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except Exception as exc:
            raise APIException(msg=str(exc), error="not_controlled_exception", http_status=status.HTTP_500_INTERNAL_SERVER_ERROR) from exc
        else:
            return Response(status=status.HTTP_200_OK)

