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

Created Date: Wednesday September 29th 2021
Author: GO and to DO Inc
E-mail: heartvoices.org@gmail.com
-----
Last Modified: Saturday, October 9th 2021, 1:53:50 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


import gspread
import logging
from functools import wraps
from playhouse.pool import PooledPostgresqlExtDatabase
from flaskapp.settings import (
    GOOGLE_SA_JSON_PATH,
    GOOGLE_USERS_SHEET_NAME_EXISTING,
    GOOGLE_USERS_SHEET_NAME_CALLS,
    GOOGLE_USERS_SPREADSHEET_ID,
    POSTGRESQL_DB_NAME,
    POSTGRESQL_HOST,
    POSTGRESQL_USER,
    POSTGRESQL_PORT,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_TEST_DB_NAME,
    POSTGRES_MAX_CONNECTIONS,
    POSTGRES_STALE_TIMEOUT,
    TEST_ENVIRONMENT
)


__all__ = ('gs_users_existing', 'gs_users_calls', 'postgres_db')


logger = logging.getLogger(__name__)


postgres_db = PooledPostgresqlExtDatabase(
    database=POSTGRESQL_TEST_DB_NAME if
    TEST_ENVIRONMENT else POSTGRESQL_DB_NAME,
    user=POSTGRESQL_USER,
    password=POSTGRESQL_PASSWORD,
    host=POSTGRESQL_HOST,
    port=POSTGRESQL_PORT,
    max_connections=POSTGRES_MAX_CONNECTIONS,
    stale_timeout=POSTGRES_STALE_TIMEOUT
)


def ensure_gc_opened(method):
    """ Ensures that connection to Google API is open for any of actions
    performed on behalf of GoogleSpreadSheed (proxy) class
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            result = method(self, *args, **kwargs) or True
        except gspread.exceptions.APIError:
            try:
                # If connection is closed (e.g. timed out),
                # lets try to reopen it!
                self.gc.login()
                self.open_spreadsheet()
                result = method(self, *args, **kwargs) or True
            except gspread.exceptions.APIError:
                logger.error(f"Error raised while appending data to {self.sheet_name}.")  # noqa: E501
                result = False
        except Exception as e:
            logger.error(f"Exception raised while accessing google spreadsheet: {e}.")  # noqa: E501
            result = False
        return result
    return wrapper


class GoogleSpreadSheet:
    """Helper class to interact with Google Spreadsheets via API"""

    gc = gspread.service_account(filename=GOOGLE_SA_JSON_PATH)

    def __init__(self, document_id='', sheet_name=''):
        self.document_id = document_id
        self.sheet_name = sheet_name
        self.spreadsheet = None
        self.worksheet = None

    def open_spreadsheet(self):
        self.spreadsheet = self.gc.open_by_key(self.document_id)
        self.worksheet = self.spreadsheet.worksheet(self.sheet_name)

    @ensure_gc_opened
    def get_all_value(self):
        return self.worksheet.get_all_values()

    @ensure_gc_opened
    def get_all_records(self):
        return self.worksheet.get_all_records()

    @ensure_gc_opened
    def append_row_to_sheet(self, row):
        """Tries to append a row to the corresponding spreadsheet/sheet_name
        and returns True if success, otherwise returns False
        """
        self.woorksheet.append_row(row)


# interacts with users spreadsheet / Existing tab
gs_users_existing = GoogleSpreadSheet(
    GOOGLE_USERS_SPREADSHEET_ID,
    GOOGLE_USERS_SHEET_NAME_EXISTING
    )


# interacts with users spreadsheet / Calls tab
gs_users_calls = GoogleSpreadSheet(
    GOOGLE_USERS_SPREADSHEET_ID,
    GOOGLE_USERS_SHEET_NAME_CALLS
    )
