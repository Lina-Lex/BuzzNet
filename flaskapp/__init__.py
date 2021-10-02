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
Last Modified: Saturday, October 2nd 2021, 3:00:56 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from flask import Flask
from .routes.ivr_url import IVRFlow
from .routes.auth import Auth

app = Flask(__name__)

###############################
##### Register blueprients ####

app.register_blueprint(IVRFlow)
app.register_blueprint(Auth,url_prefix='/authenticate')




#############################
###### ERROR HANDLER ########

@app.errorhandler(404)
def not_found(error):
    print(error)
    return ({"status_code":404,'exit_code':1,"error":f"ARE YOU LOST :: {str(error)}","message":"failed"},404)

@app.errorhandler(405)
def method_notallowed(error):
    return ({"status_code":405,'exit_code':1,"error":f"Method not allowed {str(error)}","message":"failed"},405)

@app.errorhandler(403)
def forbidden_page(error):
    return ({"status_code":403,'exit_code':1,"error":f"permission denied/ {str(error)}","message":"failed"},403)

@app.errorhandler(500)
def server_error(error):
    return ({"status_code":500,'exit_code':5,"error":f"Internal server error {str(error)}","message":"failed"},500)

@app.errorhandler(400)
def token_expired(error):
    return ({"status_code":400,'exit_code':4,"error":f"Bad Request/ Data format incorrect {str(error)}","message":"failed"},400)

@app.errorhandler(401)
def unauthorized(error):
    return ({"status_code":401,'exit_code':1,"error":f"Authorization failed,password incorrect {str(error)}","message":"failed"},401)
