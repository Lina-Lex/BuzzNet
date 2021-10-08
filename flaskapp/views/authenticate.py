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
Last Modified: Friday, October 8th 2021, 7:20:06 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from flaskapp.tools.authtools.otpstore import OTPValidator
from flask import request, abort

from flaskapp.tools.authtools.otpstore import get_authentication


otp_validator = OTPValidator()


def send_otp():
    """Generate and send OTP to the provided phone number

    :return: Raise Exception or return status dictionary
    :rtype: Any
    """

    if request.method == 'POST':
        try:
            data = request.get_json()
            if not len(data) == 1 and 'phone' not in data:
                abort(400, 'Incorrect data format')

            if otp_validator.send_otp(phone_number=data.get('phone')):
                return {
                    "message": "success",
                    'exit_code': 0
                }
        except RuntimeError as e:
            return {
                'message': 'failed',
                'exit_code': '1',
                'status_code': 501,
                'error': str(e)
            }
        except ConnectionError as e:
            abort(500, e)
    else:
        abort(405, "Only POST methods are allowed")


def validate_otp():
    """Validate OTP password provided by the user

    :return: Dictionary of predefined structure on success
    :rtype: bool

    FIXME: It is not clear why we need to return
    `message` and `exit code` here!
    Also, it is not clear why we need to return dictionary, but not
    only True/False
    """

    if request.method == "POST":
        data = request.get_json()
        if 'phone' in data and 'otp' in data and len(data) == 2:
            if otp_validator.verify_otp(
                otp_password=data.get('otp'),
                phone_number=data.get('phone')
            ):
                return {"message": "success", 'exit_code': 0}
            else:
                abort(403, 'Invalid OTP or Validation failed ')
        else:
            abort(400)
    else:
        abort(405, "Only POST methods are allowed")


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
