# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2022. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2022. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         19/12/22 9:19 PM
# Project:      CFHL Transactional Backend
# Module Name:  apps
# Description:
# ****************************************************************
from django.conf import settings
from django.apps import AppConfig


class CFHLAuth(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'oasis_auth'

    def ready(self):
        # Import Signals
        from oasis_auth.lib.signal_events import password_events
        # Code Timeout
        settings.OASIS_AUTH_CODE_TIMEOUT = getattr(settings, "OASIS_AUTH_CODE_TIMEOUT", 2)
        # High complex password
        settings.OASIS_AUTH_PASSWORD_COMPLEX = getattr(settings, "OASIS_AUTH_PASSWORD_COMPLEX", False)
        # Default length retrieve password
        settings.OASIS_AUTH_PASSWORD_LENGTH = getattr(settings, "OASIS_AUTH_PASSWORD_LENGTH", 12)
