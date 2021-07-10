import os
from os import environ
from dotenv import load_dotenv
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
twilio_account_sid = "AC2fcff6668dd972c5fcc1af4e2b368a29"
twilio_api_key_sid = "SK0064f5c1db87e9534de479a1c8b5707e"
twilio_api_key_secret = "pHkHpw7OKrjkYwB6GOrPnYT64Lu6VTTY"


# load_dotenv()
# twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
# twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
# twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')
twilio_client = Client(twilio_api_key_sid, twilio_api_key_secret,
                       twilio_account_sid)

app = Flask(__name__)

# timezone helper class to get time zone from number
from timezoneHelperClass import TimeZoneHelper

@app.route("/incoming_sms", methods=['POST'])
def sms_reply():  
    """Determine Users Phone Number from SMS and use TimeZoneHelper class to determine Time Zone."""    
    from_number = request.form['From'] 
    body = request.form['Body']
    to_number = request.form['To']

    # TODO: difference between request.form['Body'] and request.values.get('Body', None)
    #body = request.values.get('Body', None)

    print(body)
    # Start our TwiML response
    resp = MessagingResponse()

    # timezone helper class to get time zone from number
    tz_from = TimeZoneHelper(from_number)
    tz_to = TimeZoneHelper(to_number)

    # Determine the right reply for this message
    if body == 'hello':
        resp.message("Hi!")
    elif body == 'bye':
        resp.message("Goodbye")
    # Determine the right reply for this message
    elif body == 'find':
        resp.message(f"\nYour Phone Number: {from_number} \nYour time zone: {tz_from.numberToTimeZone()} My Number: {to_number} My time zone: {tz_to.numberToTimeZone()}")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
