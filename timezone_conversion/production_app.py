import os
from os import environ
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta
import gspread
import pandas as pd
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from oauth2client.service_account import ServiceAccountCredentials
from twilio.twiml.voice_response import VoiceResponse, Gather
from flask import Flask
from flask import (
  flash,
  render_template,
  redirect,
  request,
  session,
  url_for,
)
from twilio.twiml.voice_response import VoiceResponse
from flask import Response

#view_helpers.py  https://github.com/TwilioDevEd/ivr-phone-tree-python/blob/master/ivr_phone_tree_python/view_helpers.py
def twiml(resp):
    resp = Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp

def matchFromDf(dataframe, tz_from):
    """This is ugly but works, will clean up this function"""
    df = dataframe
    df[["DT Start"]] = df[["UTC start"]].apply(pd.to_datetime)
    df[["DT End"]] = df[["UTC end"]].apply(pd.to_datetime)

    # get current UTC time and find match
    now_utc = datetime.utcnow()
    tz = tz_from.numberToTimeZone() #tz = "US/Pacific"
    mask = (df['DT Start'] < now_utc) & (df['DT End'] >= now_utc) & (df['time zone'] == tz)
    result = df.loc[mask]
    print("len {}".format(result))
    match = result.head(1)
    match = int(match['Number'])
    print(f"dataframe shape {dataframe.shape}") # all results shape
    print(f"result shape: {result.shape}") # candidate matches shape
    #^^may be more candidates but have to pick one
    return match

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
print(dataframe)

# init flask app
app = Flask(__name__)

### WEBHOOK ENTRY = /welcome
@app.route('/')
def index():
    return "<h1>Hello World! Lets match some friends! Friends are good!</h1>"
  
@app.route('/welcome', methods=['POST'])
def welcome():
    response = VoiceResponse()
    with response.gather(
        num_digits=1, action=url_for('menu'), method="POST"
    ) as g:
        g.say(message="Thanks for calling the E T Phone Home Service. " +
              "Please press 1 for directions." +
              "Press 2 for a list of planets to call.", loop=3)
    return twiml(response)


# @app.route('/menu', methods=['POST'])
# def menu():
#     selected_option = request.form['Digits']
#     option_actions = {'1': _give_instructions,
#                       '2': _list_planets}

#     if option_actions.has_key(selected_option):
#         response = VoiceResponse()
#         option_actions[selected_option](response)
#         return twiml(response)

#     return _redirect_welcome()

@app.route('/menu', methods=['POST'])
def menu():
    # selected_option = request.form['Digits']
    # option_actions = {'1': voice,
    #                   '2': welcome}

    # #if option_actions.has_key(selected_option):
    # if option_actions.__contains__(selected_option):

    #     response = VoiceResponse()
    #     option_actions[selected_option](response)
    #     return twiml(response)

    #return _redirect_welcome()
    return voice()

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()
    to_number = request.form['To']
    from_number = request.form['From']  #tel = request.values['From']

    # gather = Gather(num_digits=1)
    # gather.say('To find a friend to speak with, press 1. For support, press 2.')
    # resp.append(gather)

    # timezone helper class to get time zone from number
    tz_from = TimeZoneHelper(from_number)
    tz_to = TimeZoneHelper(to_number)

########################################################
    # how to get match fro google sheet
    match = matchFromDf(dataframe, tz_from)
    print(f"test function: match is {match}")
########################################################

    #test_match = "+192533393908"
    formatMatch = "+" + str(match)
    #resp.say("you should call {}".format(formatMatch))
    resp.dial(formatMatch)

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
    # how to get match fro google sheet
    match = matchFromDf(dataframe,tz_from)
    print(f"test function: match is {match}")
########################################################
    
    # Determine the right reply for this message
    if body == 'Find friend':
        resp.message("Hi! You should call {}".format(match))
    else:
        resp.message("Goodbye")

    return str(resp)

def _redirect_welcome():
    response = VoiceResponse()
    response.say("Returning to the main menu", voice="alice", language="en-GB")
    response.redirect(url_for('welcome'))

    return twiml(response)

if __name__ == "__main__":
    app.run(debug=True)
    
