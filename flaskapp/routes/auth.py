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
Last Modified: Sunday, October 17th 2021, 2:41:35 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from flask import Blueprint
from flaskapp.views.authenticate import send_otp, validate_otp

AuthBlueprint = Blueprint('Auth', __name__)


# FIXME: endpoint /get_otp doesn't return any otp on response,
# so, `get_otp` name isn't appropriate; Its about sending otp to the user,
# and we should consider to rename get_otp to send_otp or something like this;
# However, we have related mobile app which uses this OTP functionality,
# so currently we need to leave this interface as is.
AuthBlueprint.route('/get_otp', methods=['POST'])(send_otp)
AuthBlueprint.route('/validate_otp', methods=['POST'])(validate_otp)

