from flaskivr.tools.authtools import send_otp, verify_otp
from flask import request,abort

def get_otp():
    '''Ph number should be a string in format +<country code><number>'''
    if request.method == 'POST':
        try:
            data = request.get_json()
            if data and send_otp(to = data.get('phone')):
                return {"message":"success",'exit_code':0}
        except RuntimeError as e:
            return {'message':'failed','exit_code':'1','error':str(e)}


def validate_otp():
    '''otp and phone number should be a string'''
    if request.method == "POST":
        data = request.get_json()
        if 'phone' in data and 'otp' in data and len(data) == 2:
            if verify_otp(otp = data.get('otp'),ph = data.get('phone')):
                return {"message":"success",'exit_code':0}
            else:
                abort(403,'Invalid OTP or Validation failed ')
        else:
            abort(400)