import os
from os import environ
from dotenv import load_dotenv
from datetime import datetime
import gspread
import pandas as pd
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from oauth2client.service_account import ServiceAccountCredentials
from twilio.twiml.voice_response import VoiceResponse, Gather

# timezone helper class to get time zone from number
from timezoneHelperClass import TimeZoneHelper

# acquire credentials for twilio from environment variables
load_dotenv()
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')
twilio_client = Client(twilio_api_key_sid, twilio_api_key_secret,
                       twilio_account_sid)

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/batman/Desktop/googlesheets/key/master_key.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1M-IQ-iYji-dbJSkrPehh3CMLiLGlzWZBzzGqVWzJPog/edit?usp=sharing")

# get all worksheets
sheet_instance = sheet.worksheets()

# convert to dataframe
dataframe = pd.DataFrame(sheet_instance[0].get_all_records())

# imit flask app
app = Flask(__name__)

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()
    from_number = request.form['From']  #tel = request.values['From']

    gather = Gather(num_digits=1)
    gather.say('To find a friend to speak with, press 1. For support, press 2.')
    resp.append(gather)
    
    # get number match and dial it
    #resp.dial(match)

    test_match = "+192533393908"
    #resp.say("you should call {}".format(test_match))
    resp.dial(test_match)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/voice')

    return str(resp)

@app.route("/incoming_sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.form['Body']
    to_number = request.form['To']
    from_number = request.form['From'] 

    # Start our TwiML response
    resp = MessagingResponse()

    # timezone helper class to get time zone from number
    tz_from = TimeZoneHelper(from_number)
    tz_to = TimeZoneHelper(to_number)

########################################################
    # format/clean data
    df = dataframe
    df[["DT Start"]] = df[["UTC start"]].apply(pd.to_datetime)
    df[["DT End"]] = df[["UTC end"]].apply(pd.to_datetime)

    # get current UTC time and find match
    now_utc = datetime.utcnow()
    tz = tz_from.numberToTimeZone() #tz = "US/Pacific"
    mask = (df['DT Start'] < now_utc) & (df['DT End'] >= now_utc) & (df['time zone'] == tz)
    result = df.loc[mask]
    match = result.head(1)
    match = int(match['Number'])
########################################################
    
    # Determine the right reply for this message
    if body == 'Find friend':
        resp.message("Hi! You should call {}".format(match))
    else:
        resp.message("Goodbye")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
    
