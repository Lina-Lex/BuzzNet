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
Last Modified: Saturday, October 2nd 2021, 3:02:43 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from peewee import (AutoField, TextField, DateTimeField,
                    CharField, ForeignKeyField, FloatField,
                    IntegerField)

from flaskapp.models.bases import BaseModel, DatesMixin
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


class SmartReminder(DatesMixin, BaseModel):
    id = AutoField()
    patient  = ForeignKeyField(User, backref='smart_remainders')  # noqa: E221
    reminder = ForeignKeyField(Reminder, backref='smart_remainders')

    easiness = FloatField(null=True)   # TODO: default value needed

    interval = IntegerField(column_name='interval', null=True)
    repetitions = IntegerField(column_name='repetitions', null=True)

    last_time = DateTimeField(column_name='lasttime', null=True)
    next_time = DateTimeField(column_name='nexttime', null=True)

    class Meta:
        table_name = 'smartreminders'
