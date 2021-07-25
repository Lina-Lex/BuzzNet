from flask import Blueprint
from flaskivr.view_functions.authenticate import get_otp,validate_otp

Auth = Blueprint('Auth',__name__)

Auth.route('/get_otp',methods=['POST'])(get_otp)
Auth.route('/validate_otp',methods=['POST'])(validate_otp)
