import os
from os import environ
from dotenv import load_dotenv
from datetime import datetime
import gspread
import pandas as pd
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from oauth2client.service_account import ServiceAccountCredentials
from twilio.twiml.voice_response import VoiceResponse, Gather
from flask import Flask
from flask import Response
from flask import (
  flash,
  render_template,
  redirect,
  request,
  session,
  url_for,
)

# timezone helper class to get time zone from number
from timezoneHelperClass import TimeZoneHelper

# view_helpers.py  
# https://github.com/TwilioDevEd/ivr-phone-tree-python/blob/master/ivr_phone_tree_python/view_helpers.py
def twiml(resp):
    resp = Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp

def matchFromDf(dataframe, tz_from, verbose=True):
    """This is ugly but works, will clean up this function"""
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
    
    if verbose:
        print(f"dataframe shape {dataframe.shape}") # all results shape
        print(f"result shape: {result.shape}") # candidate matches shape
    
    return match

# acquire credentials for twilio from environment variables
twilio_account_sid = "AC2fcff6668dd972c5fcc1af4e2b368a29"
twilio_api_key_sid = "SK0064f5c1db87e9534de479a1c8b5707e"
twilio_api_key_secret = "pHkHpw7OKrjkYwB6GOrPnYT64Lu6VTTY"

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
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1M-IQ-iYji-dbJSkrPehh3CMLiLGlzWZBzzGqVWzJPog/edit?usp=sharing")

# get all worksheets
sheet_instance = sheet.worksheets()

# convert to dataframe
dataframe = pd.DataFrame(sheet_instance[0].get_all_records())
print(dataframe)


# init flask app
app = Flask(__name__)

### WEBHOOK ENTRY = /welcome
@app.route('/')
def index():
    return "<h1>Hello World! Lets match some friends! Friends are good!</h1>"
  
@app.route('/welcome', methods=['POST'])
def welcome():
    """Respond to incoming phone calls with a menu of options"""
    response = VoiceResponse()
    with response.gather(
        num_digits=1, action=url_for('menu'), method="POST"
    ) as g:
        g.say(message="Thanks for calling the Heart Voices IVR System. " +
        "Please press 1 to find a match." +
        "Press 2 for help.", loop=3)
    
    return twiml(response)

@app.route('/menu', methods=['POST'])
def menu():
    selected_option = request.form['Digits']
    option_actions = {'1': "voice",
                      '2': welcome}
    result = option_actions.get(selected_option)
    response = VoiceResponse()
    response.redirect(url_for(result))
    return twiml(response)
    #return voice()

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    # Start our TwiML response
    resp = VoiceResponse()
    to_number = request.form['To']
    from_number = request.form['From']  #tel = request.values['From']

    # timezone helper class to get time zone from number
    tz_from = TimeZoneHelper(from_number)
    tz_to = TimeZoneHelper(to_number)

    # how to get match from google sheet
    match = matchFromDf(dataframe, tz_from)
    testMatch = "+19253393908"

    formatMatch = "+" + str(match)
    resp.say(
        "Connecting you to a friend. Please stay on the line."
    )
    resp.dial(testMatch, action=url_for('.end_call'))
    return Response(str(resp), 200, mimetype="application/xml")

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

    # how to get match from google sheet
    match = matchFromDf(dataframe,tz_from)
    print(f"test function: match is {match}")
    
    # Determine the right reply for this message
    if body == 'Find friend':
        resp.message("Hi! You should call {}".format(match))
    else:
        resp.message("Goodbye")

    return str(resp)

@app.route('/end_call', methods=['GET', 'POST'])
def end_call():
    """Thank user & hang up."""
    response = VoiceResponse()
    response.say(
        "Thank you for using Call Heart Voices! " + "Your voice makes a difference. Goodbye."
    )
    response.hangup()
    return Response(str(response), 200, mimetype="application/xml")

def _redirect_welcome():
    response = VoiceResponse()
    response.say("Returning to the main menu", voice="alice", language="en-GB")
    response.redirect(url_for('welcome'))

    return twiml(response)

if __name__ == "__main__":
    app.run(debug=True)
    
