# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         15/02/23 8:49
# Project:      CFHL Transactional Backend
# Module Name:  sync_users
# Description:
# ****************************************************************
from core import celery_app
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from oasis.models import Client
from typing import Any


@celery_app.task(bind=True)
def task_sync_users(app: Any):
    """
    Task to get user state, email and other variables to user table.
    :return: None
    """

    user_model = get_user_model()
    user_qs = user_model.objects.all()
    for user in user_qs:
        if hasattr(user, "profile"):
            document_id = user.profile.document_id
            try:
                oasis_customer = Client.objects.get_by_pk(pk=document_id).get()
                if user.is_active != (oasis_customer.state == "A"):
                    user.is_active = (oasis_customer.state == "A")

                if user.email != oasis_customer.main_email:
                    user.email = oasis_customer.main_email

                # Changes in profile
                if oasis_customer.segmentid is not None:
                    if user.profile.segment != oasis_customer.segmentid:
                        user.profile.segment = oasis_customer.segmentid

                if user.profile.type != oasis_customer.customer_type:
                    user.profile.type = oasis_customer.customer_type

            except Client.DoesNotExist:
                user.is_active = False
            except Exception as exc:
                raise Exception(_("Error at sync users.")) from exc
            else:
                try:
                    user.profile.save()
                except Exception as exc:
                    raise Exception(_("Error saving user profile.")) from exc
                else:
                    user.save()


