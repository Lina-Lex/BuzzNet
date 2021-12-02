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
Last Modified: Tuesday, October 19th 2021, 9:35:54 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""

import uuid
from peewee import (AutoField, TextField, DateTimeField,
                    CharField, ForeignKeyField, FloatField,
                    IntegerField)

from flaskapp.settings import OTP_PASSWORD_LENGTH
from flaskapp.models.bases import BaseModel, DatesMixin
from flaskapp.tools.authtools.authgen import generate_otp
from playhouse.postgres_ext import BinaryJSONField

USER_STATUSES = (
    ('A', 'Active'),
    ('B', 'Blocked'),
    ('D', 'Deleted')
)

GENDER_CHOICES = (
    ('M', 'Man'),  # NOTE: May be male/female more appropriate?
    ('W', 'Woman')
)


class User(DatesMixin, BaseModel):
    """ General user model """

    id = AutoField()
    username = TextField(null=True)
    gender = CharField(
        max_length=1,
        null=True,
        choices=GENDER_CHOICES
    )
    timezone = CharField(max_length=50, null=True)
    type = CharField(max_length=1, null=True)
    status = CharField(max_length=1,
                       default='A',
                       choices=USER_STATUSES)

    class Meta:
        table_name = 'users'


class PhoneNumber(DatesMixin, BaseModel):
    id = AutoField()
    number = CharField(max_length=30, unique=True)
    user = ForeignKeyField(
        User,
        null=True,
        on_delete='CASCADE'
    )

    class Meta:
        table_name = 'phone_numbers'


class Call(DatesMixin, BaseModel):
    id = AutoField()
    call_start = DateTimeField()
    call_end = DateTimeField()
    user = ForeignKeyField(
        User,
        backref='calls',
        on_delete='CASCADE'
    )

    class Meta:
        table_name = 'calls'


class HealthMetric(DatesMixin, BaseModel):
    id = AutoField()
    data = BinaryJSONField(null=True)
    user = ForeignKeyField(
        User,
        backref='health_metrics',
        on_delete='CASCADE'
    )

    class Meta:
        table_name = 'health_metrics'


class Reminder(BaseModel):
    id = AutoField()
    text = TextField(column_name='text', null=True)

    class Meta:
        table_name = 'reminders'


class OTPPassword(DatesMixin, BaseModel):
    """ Storage for OTP passwords """

    id = AutoField()
    phone_number = CharField(max_length=30)
    otp_password = CharField(
        max_length=15,
        default=lambda x: generate_otp(OTP_PASSWORD_LENGTH)
    )

    class Meta:
        table_name = 'otp_passwords'


class SmartReminder(DatesMixin, BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='smart_remainders')
    reminder = ForeignKeyField(Reminder, backref='smart_remainders')
    easiness = FloatField(null=True, default=2.3)
    interval = IntegerField(column_name='interval', null=True)
    repetitions = IntegerField(column_name='repetitions', null=True)
    last_time = DateTimeField(column_name='lasttime', null=True)
    next_time = DateTimeField(column_name='nexttime', null=True)

    class Meta:
        table_name = 'smart_reminders'


class FeedBack(DatesMixin, BaseModel):
    id = AutoField()
    phone = CharField(column_name='phone', max_length=30)
    text = TextField(column_name='text', null=True)

    class Meta:
        table_name = 'feedback'
