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
Last Modified: Saturday, October 2nd 2021, 3:00:29 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from flask import Blueprint
from flaskapp.views.ivrflow import (
    username,
    check_client_type,
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
    get_profile
)
IVRFlow=Blueprint('IVRFlow',__name__)

IVRFlow.route("/voice_joined", methods=['GET', 'POST'])(voice_joined)
IVRFlow.route("/voice", methods=['GET', 'POST'])(voice)
IVRFlow.route("/after_call", methods=['GET', 'POST'])(after_call)
IVRFlow.route("/username", methods=['GET', 'POST'])(username)
IVRFlow.route("/check_client_type", methods=['GET', 'POST'])(check_client_type)
IVRFlow.route("/save_client_type", methods=['GET', 'POST'])(save_client_type)
IVRFlow.route("/call_to_friend", methods=['GET', 'POST'])(call_to_friend)
IVRFlow.route("/find_friend_timezone", methods=['GET', 'POST'])(find_friend_timezone)
IVRFlow.route('/end_call', methods=['GET', 'POST'])(end_call)
IVRFlow.route("/call_to_operator", methods=['GET', 'POST'])(call_to_operator)
IVRFlow.route("/save_blood_pressure", methods=['GET', 'POST'])(save_blood_pressure)
IVRFlow.route("/save_feedback_service", methods=['GET', 'POST'])(save_feedback_service)
IVRFlow.route("/save_feedback", methods=['GET', 'POST'])(save_feedback)
IVRFlow.route("/search", methods=['GET', 'POST'])(search_via_google)
IVRFlow.route("/get_next_reminder", methods=['GET', 'POST'])(get_next_reminder)
IVRFlow.route("/new_user", methods=['GET', 'POST'])(new_user)
IVRFlow.route("/term_cond", methods=['GET', 'POST'])(get_term_cond)
IVRFlow.route("/privacy", methods=['GET', 'POST'])(get_privacy)
IVRFlow.route("/authenticate/get_profile", methods=['GET', 'POST'])(get_profile)
