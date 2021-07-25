from flask import Blueprint
from flaskivr.view_functions.authenticate import get_otp

Auth = Blueprint('Auth',__name__)

Auth.route('/get_otp',methods=['POST'])(get_otp)
