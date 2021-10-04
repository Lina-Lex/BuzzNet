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

Created Date: Friday October 1st 2021
Author: GO and to DO Inc
E-mail: heartvoices.org@gmail.com
-----
Last Modified: Monday, October 4th 2021, 10:32:34 am
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


import pytest
from flaskapp.models.ivr_models import (User,
                                        Reminder,
                                        SmartReminder,
                                        Call,
                                        PhoneNumber)
from flaskapp.models.utils import create_tables
from flaskapp.models.storages import postgres_db


def test_create_and_drop_tables():
    postgres_db.drop_tables([PhoneNumber, Reminder, SmartReminder, Call, User])
    tables = postgres_db.get_tables()
    assert len(tables) == 0
    create_tables([User, Call, PhoneNumber, Reminder, SmartReminder])
    tables_created = postgres_db.get_tables()
    assert 'users' in tables_created
    assert 'calls' in tables_created
    assert 'reminders' in tables_created
    assert 'phone_numbers' in tables_created
    assert 'health_metrics' in tables_created
    assert 'smart_reminders' in tables_created
