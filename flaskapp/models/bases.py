#!/usr/bin/env python3
# -*- coding:utf-8 -*-

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
