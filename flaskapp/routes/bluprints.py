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

Created Date: Sunday October 17th 2021
Author: GO and to DO Inc
E-mail: heartvoices.org@gmail.com
-----
Last Modified: Sunday, October 17th 2021, 9:30:18 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from flask import Blueprint


class BaseBlueprint(Blueprint):
    """Bluprint routes factory
    """

    def bulk_register(self, *views, route_urls=dict(), route_methods=dict()):
        """Bulk routes registeration

        :param route_urls: customize view url , defaults to dict()
        :type route_urls: dict, optional
        :param route_methods: per-view customization of allowed http-methods,
                              defaults to dict()
        :type route_methods: dict, optional
        """
        default_methods = ['GET', 'POST']
        for view in views:
            if callable(view):
                methods = route_methods.get(view.__name__, default_methods)
                url = route_urls.get(view.__name__, f"/{view.__name__}")
                self.route(url, methods=methods)(view)


class TwilioBluprint(BaseBlueprint):
    ...


class MobileAPIBluprint(BaseBlueprint):
    ...
