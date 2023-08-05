# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         27/01/23 5:30 PM
# Project:      CFHL Transactional Backend
# Module Name:  user
# Description:
# ****************************************************************
from django.contrib.auth import get_user_model
from zibanu.django.rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for authenticated user
    """

    class Meta:
        model = get_user_model()
        fields = "__all__"

