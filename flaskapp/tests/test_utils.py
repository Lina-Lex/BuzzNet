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

Created Date: Sunday October 3rd 2021
Author: GO and to DO Inc
E-mail: heartvoices.org@gmail.com
-----
Last Modified: Monday, October 4th 2021, 7:10:03 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""

import pytest
from flaskapp.tools.util import cleanup_phone_number


def test_cleanup_phone_number():
    # should be robust enough to cleanup such things as:
    sample_phone_number = "+1-8--3-9  8 492-7-3-8  "
    assert '18398492738' == cleanup_phone_number(sample_phone_number)

    with pytest.raises(ValueError):
        # Should raise an exception for malformed phone numbers
        cleanup_phone_number('+1fsdr2135323423')
