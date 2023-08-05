# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         19/06/23 13:53
# Project:      CFHL Transactional Backend
# Module Name:  signals
# Description:
# ****************************************************************
from django import dispatch

change_password = dispatch.Signal()
request_password = dispatch.Signal()

