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

Created Date: Thursday September 30th 2021
Author: GO and to DO Inc
E-mail: heartvoices.org@gmail.com
-----
Last Modified: Saturday, October 2nd 2021, 3:02:35 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


import datetime
from peewee import Proxy, Model, DateTimeField
from flaskapp.models.storages import postgres_db

db_proxy = Proxy()


# Base model for work with Database through ORM
class BaseModel(Model):
    class Meta:
        database = db_proxy  # connection with database


class DatesMixin(BaseModel):
    updated   = DateTimeField(null=True)  # noqa: E221
    created   = DateTimeField(            # noqa: E221
        default=datetime.datetime.now,
        null=True
    )

# NOTE:  Dynamic db-switching is absolutely unnecessary
# However, this construction will be useful when testing
db_proxy.initialize(postgres_db)
