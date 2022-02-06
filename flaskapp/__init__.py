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
Last Modified: Wednesday, November 10th 2021, 9:34:18 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from flask import Flask
from flaskapp.routes.ivr_url import IVRFlowBlueprint, MobileBluprint
from flaskapp.routes.auth import AuthBlueprint
from flaskapp.routes.error_handlers import error_handler_factory
from flaskapp import settings
from flaskapp.models.bases import db_proxy


def create_app():
    # create and configure the app
    app = Flask(__name__)

    # ------------ Configuration
    app.config['TESTING'] = settings.TEST_ENVIRONMENT
    app.config['SERVER_NAME'] = "heart-ivr.herokuapp.com"

    # ----------------- Open and close db-connection --------------
    # Open db connection when request has come and close when
    # response is sent
    @app.before_request
    def _db_connect():
        db_proxy.connect()

    @app.teardown_request
    def _db_close(exc):
        if not db_proxy.is_closed():
            db_proxy.close()
    # --------------------------------------------------------------

    #############################
    ###### ERROR HANDLER ######## noqa: E266

    for status_code, exit_code, error_template in zip(
        (404, 405, 403, 500, 400, 401),
        (1, 1, 1, 5, 4, 1),
        (
            "ARE YOU LOST :: {}",
            "Method not allowed {}",
            "permission denied/ {}",
            "Internal server error {}",
            "Bad Request/ Data format incorrect {}",
            "Authorization failed,password incorrect {}"
        )
    ):
        app.errorhandler(status_code)(
            error_handler_factory(
                status_code=status_code,
                exit_code=exit_code,
                error_template=error_template
            )
        )

    ###############################
    ##### Register blueprients ##### noqa: E266

    # --  TODO: Investigate potential issues with app-context
    app.register_blueprint(IVRFlowBlueprint)
    app.register_blueprint(MobileBluprint)
    app.register_blueprint(AuthBlueprint, url_prefix='/authenticate')

    return app
