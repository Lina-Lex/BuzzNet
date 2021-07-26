import os

OTP_DURATION = os.environ.get('OTP_DURATION',60)
TWILIO_ACC_SID =  os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN =  os.environ.get('TWILIO_AUTH_TOKEN')
SENDER_NUMBER = os.environ.get('SENDER_NUMBER')