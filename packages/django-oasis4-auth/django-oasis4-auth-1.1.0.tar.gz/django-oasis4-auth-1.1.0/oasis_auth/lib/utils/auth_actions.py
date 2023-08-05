# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         18/01/23 10:12 AM
# Project:      CFHL Transactional Backend
# Module Name:  auth_actions
# Description:
# ****************************************************************
from django.contrib.auth.signals import user_logged_in
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from oasis_auth.models import UserProfile
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Any


class AuthActions:
    """
    Class to encapsulate the different actions to be executed for auth package
    depending on action required.
    """

    def __init__(self, data: dict, request: Any):
        """
        Initialization method
        :param data: data dictionary with at least "data" and "action" keys.
        """
        self.__request = request
        if data is not None and {"data", "action"} <= data.keys():
            self.__data = data.get("data")
            self.__action = data.get("action")
            self.__password = data.get("password")
        else:
            raise ValidationError(_("Invalid initialization data class."))

    def __get_method(self):
        return "_" + self.__action

    def do_action(self) -> Any:
        if hasattr(self, self.__get_method()):
            # Get the method of class to invoke
            method = getattr(self, self.__get_method())
            # Invoke method
            return method()
        else:
            raise ValidationError(_("Action does not have an associated method."))

    def _register(self) -> Any:
        UserProfile.objects.create_from_customer_data(self.__data, self.__password)
        return None

    def _login(self) -> Any:
        user_logged_in.send(sender=self.__class__, user=self.__data, request=self.__request)
        token_data = RefreshToken.for_user(self.__data)
        data_return = {
            "token": str(token_data.access_token),
            "payload": token_data.payload,
            "user": {
                "full_name": self.__data.get_full_name(),
                "document_id": self.__data.profile.document_id,
                "email": self.__data.email,
                "phone": self.__data.profile.phone,
                "mobile": self.__data.profile.mobile,
                "location": self.__data.profile.location,
                "address": self.__data.profile.address,
                "last_login": self.__data.last_login,
                "type": self.__data.profile.type,
                "relationship": self.__data.profile.get_type_display(),
                "is_staff": self.__data.is_staff
            }
        }
        return data_return
