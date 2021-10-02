#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
This file is a part of heartvoices.org project.

The software embedded in or related to heartvoices.org
is provided under a some-rights-reserved license. This means
that Users are granted broad rights, including but not limited
to the rights to use, execute, copy or distribute the software,
to the extent determined by such license. The terms of such
license shall always prevail upon conflicting, divergent or
inconsistent provisions of these Terms. In particular, heartvoices.org
and/or the software thereto related are provided under a GNU GPLv3 license,
allowing Users to access and use the software’s source code.
Terms and conditions: https://www.goandtodo.org/terms-and-conditions

Created Date: Sunday September 26th 2021
Author: GO and to DO Inc
E-mail: heartvoices.org@gmail.com
-----
Last Modified: Saturday, October 2nd 2021, 3:02:05 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


import os

OTP_DURATION = os.environ.get('OTP_DURATION',60)
TWILIO_ACC_SID =  os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN =  os.environ.get('TWILIO_AUTH_TOKEN')
SENDER_NUMBER = os.environ.get('SENDER_NUMBER')