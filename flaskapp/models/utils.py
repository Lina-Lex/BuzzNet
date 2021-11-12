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
Last Modified: Friday, October 15th 2021, 11:01:24 am
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from flaskapp.models.storages import postgres_db
from flaskapp.models.ivr_models import (User, UserToken, HealthMetric,
                                        Call, SmartReminder, Reminder,
                                        OTPPassword, PhoneNumber, FeedBack)


def create_tables(tables=None):
    """Create specific tables if they do not exist

    :param tables: a list of tables (items are subclasses of peewee.Model),
                   defaults to None
    :type tables: List[peewee.Model], optional
    """

    if tables:
        with postgres_db:
            postgres_db.create_tables(tables)


def init_db():
    """Create all necessary tables for the project
    """

    create_tables([User, UserToken, HealthMetric, Call, Reminder,
                   SmartReminder, OTPPassword, PhoneNumber, FeedBack])


def drop_all_tables():
    """Drop all tables related to the project
    """

    postgres_db.drop_tables([User, UserToken, HealthMetric, Call, Reminder,
                             SmartReminder, OTPPassword, PhoneNumber, FeedBack])
