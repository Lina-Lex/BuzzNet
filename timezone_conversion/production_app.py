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

# creds
twilio_account_sid = "AC2fcff6668dd972c5fcc1af4e2b368a29"
twilio_api_key_sid = "SK0064f5c1db87e9534de479a1c8b5707e"
twilio_api_key_secret = "pHkHpw7OKrjkYwB6GOrPnYT64Lu6VTTY"

# acquire credentials for twilio from environment variables
# load_dotenv()
# twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
# twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
# twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')
twilio_client = Client(twilio_api_key_sid, twilio_api_key_secret,
                       twilio_account_sid)
# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/batman/Desktop/googlesheets/key/master_key.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
#sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1gIDRAw203QCWp_8mGo6sZQi50vziKBsQShbd0txIktU/edit?usp=sharing")
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1M-IQ-iYji-dbJSkrPehh3CMLiLGlzWZBzzGqVWzJPog/edit?usp=sharing")
# get all worksheets
sheet_instance = sheet.worksheets()

# convert to dataframe
dataframe = pd.DataFrame(sheet_instance[0].get_all_records())
print(f"*** ALL WORKSHEETS *** {sheet_instance}")
print(f"df {dataframe.head()}")

app = Flask(__name__)

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()
    #tel = request.values['From']
    from_number = request.form['From'] 

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
    #body = request.values.get('Body', None)
    body = request.form['Body']
    to_number = request.form['To']
    from_number = request.form['From'] 

    # Start our TwiML response
    resp = MessagingResponse()

    # timezone helper class to get time zone from number
    tz_from = TimeZoneHelper(from_number)
    tz_to = TimeZoneHelper(to_number)


    df = dataframe
    tzs_df = pd.read_csv("/home/batman/Desktop/BuzzNet-main/timezone_conversion/data/tzmapping.csv")
    tzs_df.index = tzs_df['State'] # important
    pd.set_option('display.float_format', lambda x: '%.0f' % x)
    #df.drop('time zone', axis=1, inplace=True)
    df.rename(columns={'Unnamed: 0': 'Username'}, inplace=True)
    df[["DT Start"]] = df[["UTC start"]].apply(pd.to_datetime)
    df[["DT End"]] = df[["UTC end"]].apply(pd.to_datetime)
    now_utc = datetime.utcnow()
    #tz = TimeZoneHelper(number)
    tz = "US/Pacific"
    mask = (df['DT Start'] < now_utc) & (df['DT End'] >= now_utc) & (df['time zone'] == tz)
    result = df.loc[mask]
    match = result.head(1)
    # print(match['Number'])
    match = int(match['Number'])

    # path to users data : /home/batman/Desktop/BuzzNet-main/timezone_conversion/data/users_test.csv
    # Determine the right reply for this message
    if body == 'Find':
        resp.message("Hi! You should call {}".format(match))
    elif body == 'bye':
        resp.message("Goodbye")
    # elif body == 'find':
    #     resp.message(f"\nYour Phone Number: {from_number} \nYour time zone: {tz_from.numberToTimeZone()} My Number: {to_number} My time zone: {tz_to.numberToTimeZone()}")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
    
