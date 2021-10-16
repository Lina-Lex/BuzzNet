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
Last Modified: Saturday, October 16th 2021, 8:26:20 am
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""

import pytest
import datetime
from flaskapp.models.ivr_models import OTPPassword
from flaskapp.tools.authtools.authgen import generate_otp
from flaskapp.tools.authtools.otpstore import OTPValidator
from flaskapp.tools.utils import cleanup_phone_number


def test_generate_otp():
    password = generate_otp(10)
    assert len(password) == 10
    assert isinstance(password, str)
    assert password.isnumeric()

@pytest.fixture
def test_OTPValidator(monkeypatch):
    user_phone_number = '+1123456123'
    cleaned_user_number = cleanup_phone_number(user_phone_number)

    # ----  mock twilio-related method (we hope twilio works well)
    def mock_send_message_by_twilio(self,  phone_number='',  message=''):
        return True if phone_number.isnumeric() and message else False

    monkeypatch.setattr(
        'flaskapp.tools.authtools.otpstore.OTPValidator.send_message_by_twilio',  # noqa: E501
        mock_send_message_by_twilio
    )

    # drop all OTPPassowrds with test phone number
    OTPPassword.delete().where(
        OTPPassword.phone_number == cleaned_user_number
    )

    otp_validator = OTPValidator()

    pre_generation_time = datetime.datetime.now()
    # --- Test send_otp method
    assert otp_validator.send_otp(user_phone_number)

    # --- Once send_otp method called, OTP-password instance should be created
    assert OTPPassword.select().where(
        OTPPassword.phone_number == cleaned_user_number
    ).exists()

    # --- creation date of the otp password should be in a specific interval
    otp_query = OTPPassword.select().where(
        OTPPassword.phone_number == cleaned_user_number &
        OTPPassword.created > pre_generation_time &
        OTPPassword.created < datetime.datetime.now()
    )

    assert otp_query.exists()

    # --- test verify_otp helper method
    otp_object = otp_query.first()
    assert otp_validator.verify_otp(otp_object.otp_passowrd)
