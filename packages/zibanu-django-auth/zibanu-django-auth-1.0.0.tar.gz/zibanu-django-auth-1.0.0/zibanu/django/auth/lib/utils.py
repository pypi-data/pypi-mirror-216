# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         13/05/23 10:23
# Project:      Zibanu - Django
# Module Name:  utils
# Description:  Utils tools for auth module
# ****************************************************************
from typing import Any
from zibanu.django.utils import get_user as zb_get_user


def get_user(user: Any) -> Any:
    """
    Function to get User objecto from TokenUser or another object.
    :param user: Any: User object to be converted
    :return: User: User object.
    """
    return zb_get_user(user=user)


def get_user_object(user: Any) -> Any:
    """
    Legacy function. This function will be discontinued in future versions.
    :param user: Any: User object from request or auth to be returned
    :return: User: User object
    """
    return zb_get_user(user=user)