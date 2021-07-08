import os
import os
from dotenv import load_dotenv
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')
twilio_client = Client(twilio_api_key_sid, twilio_api_key_secret,
                       twilio_account_sid)

app = Flask(__name__)

# timezone helper class to get time zone from number
from timezoneHelperClass import TimeZoneHelper

@app.route("/incoming_sms", methods=['POST'])
def sms_reply(): 
    """Determine Users Phone Number from SMS and use TimeZoneHelper class to determine Time Zone."""    
    
    # Use this data in your application logic
    from_number = request.form['From']
    to_number = request.form['To']
    body = request.form['Body']

    # Start our TwiML response
    resp = MessagingResponse()

    # timezone helper class to get time zone from number
    tz = TimeZoneHelper(from_number)

    # Determine the right reply for this message
    if body == 'find' or 'Find':
        resp.message(f"\nYour Phone Number: {from_number} \nYour timezone: {tz.numberToTimeZone()}")
    elif body == 'bye':
        resp.message("Goodbye")
    else:
        resp.message("I didn't catch that. Sorry.")

    #elif "alex" in body:
        #while True:
            # resp.message(alex) :)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
