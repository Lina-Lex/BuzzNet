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
Last Modified: Thursday, October 14th 2021, 7:25:07 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""

import datetime
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException, TwilioException
from flaskapp.settings import (OTP_DURATION,
                               TWILIO_ACCOUNT_SID,
                               TWILIO_AUTH_TOKEN,
                               TWILIO_MAIN_PHONE_NUMBER)
from flaskapp.models.ivr_models import OTPPassword
from flaskapp.tools.util import cleanup_phone_number
from logging import getLogger

logger = getLogger(__name__)


class OTPValidator:
    """ Helper class to perform OTP validation """

    def send_message_by_twilio(self, phone_number='',  message=''):
        """Send message using Twilio

        :param phone_number: where to send the message, defaults to ''
        :type phone_number: str, optional
        :param message: what to send, defaults to ''
        :type message: str, optional
        :return: True -- message was succesfully sent, otherwise -- False
        :rtype: bool
        """

        if message and phone_number:
            try:
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                client.messages.create(
                    to=phone_number,
                    from_=TWILIO_MAIN_PHONE_NUMBER,
                    body=message
                )
            except (TwilioRestException) as e:
                logger.error(f'[X] Fatal error,[X] Detailed error:- ({e}) ')
                return False
            except TwilioException as e:
                logger.error(f"unable to connect to message server :- {e}")
                return False
            return True
        return False

    def send_otp(self, phone_number=''):
        """Send OTP to provided phone number

        :param phone_number: phone number in the form +xxxx, defaults to ''
        :type phone_number: str, optional
        :return: True -- if OTP was succesfully sent, otherwise -- False
        :rtype: bool
        """

        otp_object = OTPPassword.create(
            phone_number=cleanup_phone_number(phone_number)
        )
        message = f"Your One Time Password (OTP) is: {otp_object.otp_password}"
        return self.send_message_by_twilio(
            phone_number='+' + otp_object.phone_number,
            message=message
        )

    def verify_otp(self, otp_password='', phone_number=''):
        """Verify OTP that was previously sent to the user

        :param otp_password: otp to verify, defaults to ''
        :type otp_password: str, optional
        :param phone_number: phone to which otp was sent, defaults to ''
        :type phone_number: str, optional
        :return: True if OTP was verified, otherwise False
        :rtype: bool
        """

        cleaned_phone_number = cleanup_phone_number(phone_number)
        current_date = datetime.datetime.now()
        time_delta = datetime.timedelta(seconds=OTP_DURATION)
        verified = OTPPassword.select().where(
            OTPPassword.phone_number == cleaned_phone_number &
            OTPPassword.otp_password == otp_password &
            OTPPassword.created >= current_date - time_delta).exists()

        # TODO: When verified we need to create public/private keypair
        # to sign all further requests to the api
        return verified


# TODO: should be removed in the nearest feature (currently, orphaned function)
def get_authentication(phone):
    with sqlite3.connect('otp.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT Verify FROM otp_info WHERE Phone =?", (phone,))
        result = cursor.fetchone()
        verify = False
        cursor.execute('UPDATE otp_info SET Verify=(?) WHERE Phone =(?)', (verify, phone))
        db.commit()
        return result
