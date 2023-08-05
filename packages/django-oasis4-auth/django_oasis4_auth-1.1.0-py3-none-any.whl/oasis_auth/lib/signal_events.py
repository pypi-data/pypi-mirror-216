# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         19/06/23 13:55
# Project:      CFHL Transactional Backend
# Module Name:  signal_events
# Description:
# ****************************************************************
from django.dispatch import receiver
from oasis_auth.lib.signals import *
from typing import Any
from zibanu.django.logging.models import Log
from zibanu.django.utils import get_ip_address

@receiver(change_password)
@receiver(request_password)
def password_events(sender: Any, user: Any, **kwargs) -> None:
    """
    Generic event for change or request password
    :param sender: sender class
    :param user: user object
    :param kwargs: kwargs dict
    :return:
    """
    class_name = sender.__name__
    ip_address = get_ip_address(kwargs.get("request", None))
    action = kwargs.get("action", "")
    log = Log(user=user, sender=class_name, action=action, ip_address=ip_address)
    log.save()