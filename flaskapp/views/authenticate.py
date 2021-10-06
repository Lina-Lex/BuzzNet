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

Created Date: Wednesday October 6th 2021
Author: GO and to DO Inc
E-mail: heartvoices.org@gmail.com
-----
Last Modified: Wednesday, October 6th 2021, 8:35:35 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from flaskapp.tools.authtools import send_otp, verify_otp
from flask import request, abort

from flaskapp.tools.authtools.otpstore import get_authentication


def get_otp():
    '''Ph number should be a string in format +<country code><number>'''
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not len(data) == 1 and not 'phone' in data:
                msg = f'Incorrect data format'
                abort(400, msg)
            if send_otp(to=data.get('phone')):
                return {"message": "success", 'exit_code': 0}
        except RuntimeError as e:
            return {'message': 'failed', 'exit_code': '1', 'status_code': 501, 'error': str(e)}
        except ConnectionError as e:
            abort(500, e)


def validate_otp():
    '''otp and phone number should be a string'''
    if request.method == "POST":
        data = request.get_json()
        if 'phone' in data and 'otp' in data and len(data) == 2:
            if verify_otp(otp=data.get('otp'), ph=data.get('phone')):
                return {"message": "success", 'exit_code': 0}
            else:
                abort(403, 'Invalid OTP or Validation failed ')
        else:
            abort(400)


def is_user_authenticated(phone) -> (bool, str):
    verify, message = None, None
    res = get_authentication(phone)
    if res is not None:
        verify = res[0]
        if not verify:
            message = "otp verification error"
        else:
            message = "Otp verification passed successfully"
    else:
        message = "Phone number of request is not equal for request number"

    return verify, message