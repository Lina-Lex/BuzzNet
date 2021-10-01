#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flaskapp.models.storages import postgres_db


def create_tables(tables=None):
    """Create specific tables if they do not exist

    :param tables: a list of tables (items are subclasses of peewee.Model),
                   defaults to None
    :type tables: List[peewee.Model], optional
    """

    if tables:
        with postgres_db:
            postgres_db.create_tables(tables)

