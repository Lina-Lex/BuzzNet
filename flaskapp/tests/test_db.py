#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pytest
from flaskapp.models.ivr_models import (User,
                                        Reminder,
                                        SmartReminder,
                                        Call,
                                        PhoneNumber,
                                        postgres_db)
from flaskapp.models.utils import create_tables



def test_create_tables(monkeypatch):
    create_tables([User, Call, PhoneNumber, Reminder, SmartReminder])
    tables_created = postgres_db.get_tables()
    assert 'users' in tables_created
    assert 'calls' in tables_created
