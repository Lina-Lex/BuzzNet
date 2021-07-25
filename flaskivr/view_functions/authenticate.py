from flaskivr.tools.authtools import send_otp, verify_otp
from flask import request,abort

def get_otp():
    if request.method == 'POST':
        data = request.get_json()
        if data and send_otp(data.get('phone')):
            return {"message":"success"}
        
