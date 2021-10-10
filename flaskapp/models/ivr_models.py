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
Last Modified: Sunday, October 10th 2021, 6:05:17 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from peewee import (AutoField, TextField, DateTimeField,
                    CharField, ForeignKeyField, FloatField,
                    IntegerField)

from flaskapp.settings import OTP_PASSWORD_LENGTH
from flaskapp.models.bases import BaseModel, DatesMixin
from flaskapp.tools.authtools.authgen import generate_otp
from playhouse.postgres_ext import BinaryJSONField


class User(DatesMixin, BaseModel):
    """ General user model """

    id        = AutoField()                             # noqa: E221
    username  = TextField(null=True)                    # noqa: E221
    gender    = CharField(max_length=1, null=True)      # noqa: E221
    timezone  = CharField(max_length=50, null=True)     # noqa: E221
    type      = CharField(max_length=1, null=True)      # noqa: E221

    class Meta:
        table_name = 'users'


class PhoneNumber(DatesMixin, BaseModel):
    id      = AutoField()                            # noqa: E221
    number  = CharField(max_length=30, unique=True)  # noqa: E221
    user    = ForeignKeyField(                       # noqa: E221
        User,
        null=True,
        on_delete='CASCADE'
    )

    class Meta:
        table_name = 'phone_numbers'


class Call(DatesMixin, BaseModel):
    id         = AutoField()              # noqa: E221
    call_start = DateTimeField()          # noqa: E221
    call_end   = DateTimeField()          # noqa: E221
    user       = ForeignKeyField(         # noqa: E221
        User,
        backref='calls',
        on_delete='CASCADE'
    )

    class Meta:
        table_name = 'calls'


class HealthMetric(DatesMixin, BaseModel):
    id         = AutoField()               # noqa: E221
    data       = BinaryJSONField()         # noqa: E221
    user       = ForeignKeyField(          # noqa: E221
        User,
        backref='health_metrics',
        on_delete='CASCADE'
    )

    class Meta:
        table_name = 'health_metrics'


class Reminder(BaseModel):
    id   = AutoField()                      # noqa: E221
    text = TextField(column_name='text', null=True)

    class Meta:
        table_name = 'reminders'


class OTPPassword(DatesMixin, BaseModel):
    """ Storage for OTP passwords """

    id           = AutoField()                              # noqa: E221
    phone_number = CharField(max_length=30)                 # noqa: E221
    otp_password = CharField(                               # noqa: E221
        max_length=15,
        default=lambda x: generate_otp(OTP_PASSWORD_LENGTH)
    )

    class Meta:
        table_name = 'otp_passwords'


class UsersKeypair(BaseModel):
    """Storage for private and public keys associated with the User
    """

    # TODO: Public and Private keys generator needed
    id          = AutoField()                       # noqa: E221
    private_key = CharField(null=False)
    public_key  = CharField(null=False)             # noqa: E221
    user        = ForeignKeyField(User, null=True)  # noqa: E221

    class Meta:
        table_name = 'users_keypairs'


class SmartReminder(DatesMixin, BaseModel):
    id          = AutoField()                                 # noqa: E221
    patient     = ForeignKeyField(User,                       # noqa: E221
                                  backref='smart_remainders')
    reminder    = ForeignKeyField(Reminder,                   # noqa: E221
                                  backref='smart_remainders')

    easiness    = FloatField(null=True, default=2.3)          # noqa: E221

    interval    = IntegerField(column_name='interval',        # noqa: E221
                               null=True)
    repetitions = IntegerField(column_name='repetitions', null=True)

    last_time   = DateTimeField(column_name='lasttime',       # noqa: E221
                                null=True)
    next_time   = DateTimeField(column_name='nexttime',       # noqa: E221
                                null=True)

    class Meta:
        table_name = 'smart_reminders'
