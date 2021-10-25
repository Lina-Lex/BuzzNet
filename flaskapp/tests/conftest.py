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

Created Date: Monday October 25th 2021
Author: GO and to DO Inc
E-mail: heartvoices.org@gmail.com
-----
Last Modified: Monday, October 25th 2021, 9:21:33 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


import pytest
from flaskapp import create_app
from flaskapp.models.utils import init_db, drop_all_tables


@pytest.fixture(scope='module')
def init_test_db():
    """Database initialization fixture

    Executes once a time for all tests in this module.
    """
    # SetUp...
    drop_all_tables()
    init_db()
    yield   # Here we started to execute tests
    # TearDown...  # drop all test tables were created during tests
    drop_all_tables()


@pytest.fixture(scope='module')
def client():
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!
