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
Last Modified: Saturday, October 2nd 2021, 3:02:28 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from flask import Blueprint
from flaskapp.views.authenticate import get_otp,validate_otp

Auth = Blueprint('Auth',__name__)

Auth.route('/get_otp',methods=['POST'])(get_otp)
Auth.route('/validate_otp',methods=['POST'])(validate_otp)
