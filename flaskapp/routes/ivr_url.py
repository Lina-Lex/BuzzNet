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
Last Modified: Monday, October 25th 2021, 8:57:17 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from twilio.twiml.voice_response import VoiceResponse
from flaskapp.routes.bluprints import TwilioBluprint, MobileAPIBluprint
from flaskapp.views.ivrflow import (
    get_username,
    get_client_type,
    save_client_type,
    call_to_friend,
    find_friend_timezone,
    end_call,
    call_to_operator,
    save_blood_pressure,
    save_feedback_service,
    save_feedback,
    search_via_google,
    get_next_reminder,
    voice_joined,
    voice,
    after_call,
    get_term_cond,
    get_privacy,
    get_profile,
    new_user,
    unsubscribe
)


def ensure_twilio_voice_response(response):
    if not response.get_data(as_text=True).strip():
        response.set_data(str(VoiceResponse()))
    return response


IVRFlowBlueprint = TwilioBluprint('IVRFlowBlueprint', __name__)
MobileBluprint = MobileAPIBluprint('MobileAPIBluprint', __name__)


IVRFlowBlueprint.after_request(ensure_twilio_voice_response)

IVRFlowBlueprint.bulk_register(
    *(
        voice_joined,
        voice,
        after_call,
        get_username,
        save_client_type,
        find_friend_timezone,
        end_call,
        save_blood_pressure,
        save_feedback_service
    ),

)


MobileBluprint.bulk_register(
    *(
        get_username,
        get_client_type,
        call_to_friend,
        call_to_operator,
        save_feedback,
        search_via_google,
        get_next_reminder,
        new_user,
        unsubscribe,
        get_term_cond,
        get_privacy,
        get_profile
    ),
    {
        'get_username': 'username',
        'get_client_type': 'check_client_type',
        'search_via_google': 'search',
        'get_term_cond': 'term_cond',
        'get_privacy': 'privacy',
        'get_profile': '/authenticate/get_profile'
    }
)
