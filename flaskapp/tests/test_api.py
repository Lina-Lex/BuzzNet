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

Created Date: Saturday October 2nd 2021
Author: GO and to DO Inc
E-mail: heartvoices.org@gmail.com
-----
Last Modified: Saturday, October 2nd 2021, 2:56:01 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""

import time
from flaskapp.views.ivrflow import get_term_cond, get_privacy
from flaskapp import app
from flask import Response


def test_get_term_cond():
    with app.app_context():
        result = get_term_cond()
    assert isinstance(result, Response) is True
    assert result.status_code == 200


def test_get_privacy():
    with app.app_context():
        result = get_privacy()
    assert isinstance(result, Response) is True
    assert result.status_code == 200


def test_get_privacy_caching():
    with app.app_context():
        start = time.time()
        result1 = get_privacy()
        end = time.time()
        result2 = get_privacy()
        final = time.time()
    assert final - end >= end - start
    assert result1 == result2
