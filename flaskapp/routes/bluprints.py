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
Last Modified: Monday, October 25th 2021, 9:59:54 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from flask import Blueprint


class BaseBlueprint(Blueprint):
    """Bluprint routes factory
    """

    def bulk_register(self, *views, route_urls=dict(), route_methods=dict()):
        """Bulk registeration of view functions

        This helper method is useful when we need to register
        a series of view function and attach them to the url-endpoints
        having the same names as these functions have, i.e.
        view_func1   -> /view_func1
        view_func2   -> /view_func2 etc

        `bulk_register` just uses `.route` Blueprint method
        and applied it to all passed functions within the`views` array.

        If one need to override this default behavior of registration
        which assigns (view_func -> /view_func, with allowed GET and POST
        methods), one can provide mapping variable and change this default
        behavior on per-view basis:

        if `route_urls` dictionary includes record
        `"view_function_name": "one1"`, default registration behavior will be
        overriden: registered url-endpoint for
        `view_function_name` will be `/one1`.

        The same technique is used to override allowed methods;
        Note: all views registered by `bulk_register` method by default have
        have GET and POST methods as allowed.

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
                url = route_urls.get(view.__name__, f"{view.__name__}")
                url = '/' + url if not url.startswith('/') else url
                self.route(url, methods=methods)(view)


class TwilioBluprint(BaseBlueprint):
    ...


class MobileAPIBluprint(BaseBlueprint):
    ...
