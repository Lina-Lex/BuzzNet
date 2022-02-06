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
Last Modified: Friday, October 8th 2021, 10:35:34 am
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""

import os

# import flaskapp.setenvs
# ---------- Twilio configuration ------------------

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_MAIN_PHONE_NUMBER = os.environ.get("TWILIO_MAIN_PHONE_NUMBER", "")

# Optional phone number
TWILIO_OPT_PHONE_NUMBER = os.environ.get("TWILIO_OPT_PHONE_NUMBER", "")

# magic_number for twilio call logs
MAGIC_NUMBER = 7

# ---------- Google API Configs --------------------

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

# Google custom search ID
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID", "")

# Max number of items to return when do searching
GOOGLE_CSE_MAX_NUM = 3

# Path to the json file with Google service account credentials
GOOGLE_SA_JSON_PATH = os.environ.get("GOOGLE_SA_JSON_PATH", "")

# ---------- Google docs IDs -----------------------

GOOGLE_USERS_SPREADSHEET_NAME = "Users"
GOOGLE_USERS_SPREADSHEET_ID = "1rmfzTtQnQwzZHhPciTFmKIXju2b_ScH5mVvXhG_mlkM"
GOOGLE_USERS_SHEET_NAME_EXISTING = "Existing"
GOOGLE_USERS_SHEET_NAME_CALLS = "Calls"

GOOGLE_FEEDBACK_SPREADSHEET_NAME = "feedback"
GOOGLE_FEEDBACK_SPREADSHEET_ID = ""
GOOGLE_FEEDBACK_SHEET_NAME = "service"

GOOGLE_HEALTH_DB_SPREADSHEET_NAME = "health_metrics"
GOOGLE_HEALTH_DB_SPREADSHEET_ID = ""
GOOGLE_HEALTH_DB_SHEET_NAME = "blood_pressure"

# ------------ DATABASE CONFIGURATION --------------
POSTGRESQL_DB_NAME = 'goanddo'
POSTGRESQL_USER = 'postgres'
POSTGRESQL_PASSWORD = os.environ.get("POSTGRESQL_PASSWORD", "123")
POSTGRESQL_HOST = '127.0.0.1'
POSTGRESQL_PORT = 5432

POSTGRESQL_TEST_DB_NAME = 'goanddo_test'

POSTGRES_MAX_CONNECTIONS = 32

# The number of seconds allowed to any of connections to postgres
POSTGRES_STALE_TIMEOUT = 300

# Heroku specific settings
POSTGRESQL_URL = os.environ.get("DATABASE_URL", "")
# --------------------------------------------------


# ------------- Auth configuraion ------------------

OTP_DURATION = os.environ.get('OTP_DURATION', 60)
OTP_PASSWORD_LENGTH = 6

# -----------  Helper constants --------------------
# True if we run the script on Heroku, otherwise False.
ON_HEROKU = 'HEROKU' in os.environ

ORDINAL_NUMBERS = [
    'first',
    'second',
    'third',
    'forth',
    'fifth',
    'sixth',
    'seventh',
    'eighth',
    'ninth',
    'tenth'
]

# -- Override some values for Heroku environment ---

if ON_HEROKU:
    # TODO: Put URL parsing function into helper function
    import urllib.parse

    urllib.parse.uses_netloc.append('postgres')
    url = urllib.parse.urlparse(POSTGRESQL_URL)
    POSTGRESQL_DB_NAME = url.path[1:]
    POSTGRESQL_USER = url.username
    POSTGRESQL_PASSWORD = url.password
    POSTGRESQL_HOST = url.hostname
    POSTGRESQL_PORT = url.port

# ---------

# Set to True for testing (use testing database)
TEST_ENVIRONMENT = "TEST_ENVIRONMENT" in os.environ
