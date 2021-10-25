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
Last Modified: Monday, October 25th 2021, 9:28:40 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


import pytest
import time
from flaskapp.views.ivrflow import get_term_cond, get_privacy, unsubscribe
from flaskapp.models.ivr_models import User, PhoneNumber
from flask import Response, url_for


@pytest.mark.usefixtures("client")
def test_get_term_cond():
    result = get_term_cond()
    assert isinstance(result, Response) is True
    assert result.status_code == 200


def test_get_term_cond_request(client):
    result = client.get(
        url_for('MobileAPIBluprint.get_term_cond')
    )
    assert result.status_code == 200


@pytest.mark.usefixtures("client")
def test_get_privacy():
    result = get_privacy()
    assert isinstance(result, Response) is True
    assert result.status_code == 200


@pytest.mark.usefixtures("client")
def test_get_privacy_caching():
    start = time.time()
    result1 = get_privacy()
    end = time.time()
    result2 = get_privacy()
    final = time.time()
    assert final - end >= end - start
    assert result1 == result2


@pytest.mark.usefixtures("init_test_db", "client")
def test_unsubscribe():
    ...
    # TODO: Should be implemented!


def test_save_client_type(monkeypatch):
    def mocked_google_proxy_obj():
        ...
    mocked_google_proxy_obj.append_row_to_sheet = lambda x: None
    mocked_google_proxy_obj.update_cell = lambda x, y, z, w: None

    monkeypatch.setattr(
        'flaskapp.core.ivr_core.gs_users_existing',
        mocked_google_proxy_obj
    )

    # TODO: test is not completed

    # with app.app_context():
    #     save_client_url = url_for('save_client_type')
    #     breakpoint()
    #     assert False

    #     with app.test_client() as api_client:
    #         ...
