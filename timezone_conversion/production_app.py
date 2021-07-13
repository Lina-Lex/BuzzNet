import os
from os import environ
from dotenv import load_dotenv
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/batman/Desktop/googlesheets/key/master_key.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1gIDRAw203QCWp_8mGo6sZQi50vziKBsQShbd0txIktU/edit?usp=sharing")

# get the first sheet of the Spreadsheet
#sheet_instance = sheet.get_worksheet(0)

# get all worksheets
sheet_instance = sheet.worksheets()

# convert to dataframe
dataframe = pd.DataFrame(sheet_instance[0].get_all_records())
#print(dataframe.head())

load_dotenv()
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')
twilio_client = Client(twilio_api_key_sid, twilio_api_key_secret,
                       twilio_account_sid)

# timezone helper class to get time zone from number
from timezoneHelperClass import TimeZoneHelper

app = Flask(__name__)

@app.route("/incoming_sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'hello':
        resp.message("Hi!")
    elif body == 'bye':
        resp.message("Goodbye")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
    