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

Created Date: Friday October 15th 2021
Author: GO and to DO Inc
E-mail: heartvoices.org@gmail.com
-----
Last Modified: Saturday, October 16th 2021, 8:22:17 am
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""

import pytest
import datetime
from flaskapp.core.ivr_core import save_data_to_postgres, save_new_user
from flaskapp.models.ivr_models import User, HealthMetric, PhoneNumber
from flaskapp.models.utils import init_db, drop_all_tables
from flaskapp.tools.utils import cleanup_phone_number


@pytest.fixture(scope='module')
def init_test_db():
    # SetUp...
    drop_all_tables()
    init_db()
    yield
    # TearDown...
    drop_all_tables()


@pytest.mark.usefixtures("init_test_db")
def test_save_data_to_postgres():
    user_phone_number = '+123456123456'
    user = User.create()
    PhoneNumber.create(number=user_phone_number, user=user)
    current_date = datetime.datetime.now()

    save_data_to_postgres('sbp', 100, user_phone_number, date=current_date)

    with pytest.raises(ValueError):
        save_data_to_postgres('sbp', 100, user_phone_number, date=current_date)

    hm_objs = HealthMetric.select().where(
        (HealthMetric.user == user) & (HealthMetric.created == current_date)
    )
    assert hm_objs.exists()
    assert hm_objs.first().data['sbp'] == 100

    # if we feature_name is a legal field of User model, override its value
    user.type = 'A'  # Set fake user type
    user.save()

    # Override user's type
    save_data_to_postgres(
        'type',
        'S',
        user_phone_number,
        date=current_date
    )

    # reload user (updated) instance from db
    user = type(user).get(user._pk_expr())
    assert user.type == 'S'


    # Save health objects at different date
    save_data_to_postgres(
        'sbp',
        101,
        user_phone_number,
        date=datetime.datetime.now()
    )

    hm_objs = HealthMetric.select().where(
        (HealthMetric.user == user) & (HealthMetric.created >= current_date)
    )
    assert hm_objs.count() == 2
    assert hm_objs[0].data['sbp'] in [100, 101]
    assert hm_objs[1].data['sbp'] in [100, 101]


@pytest.mark.usefixtures("init_test_db")
def test_save_new_user(monkeypatch):
    def mocked_google_proxy_obj():
        ...
    mocked_google_proxy_obj.append_row_to_sheet = lambda x: None

    def mocked_send_mail(msg, phone=''):
        return True if msg and phone else False

    monkeypatch.setattr(
        'flaskapp.core.ivr_core.send_mail',
        mocked_send_mail
    )

    monkeypatch.setattr(
        'flaskapp.core.ivr_core.gs_users_existing',
        mocked_google_proxy_obj
    )
    user_phone_number = "+123456"
    save_new_user(phone_number=user_phone_number)
    assert PhoneNumber.select().where(
        PhoneNumber.number == cleanup_phone_number(user_phone_number)
    ).exists()
