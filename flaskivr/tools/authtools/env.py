import os
from posix import environ

OTP_DURATION = os.environ.get('OTP_DURATION',300)
TWILIO_ACC_SID =  os.environ.get('TWILIO_ACCOUNT_SID','AC52d321df2eb36f8cc4091e57e59f15b3')
TWILIO_AUTH_TOKEN =  os.environ.get('TWILIO_AUTH_TOKEN','445a43914e24f5b83bda5915db0fea54')
SENDER_NUMBER = os.environ.get('SENDER_NUMBER','+14159186834')
