################################
######## MUST BE RUN WITH NGROK 
# >>> ngrok http 5000
# kevins twilio number: (925) 291-5450
# v0
################################
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

# see "/helpers/helper.txt and "helpers/webhookSMS.png" and "helpers/nbrok.png" for explanation of how to set this up
@app.route("/incoming_sms", methods=['POST'])
def sms_reply():  
    """Respond to incoming calls with a simple text message."""
 
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
        resp.message("Your Phone Number: {} \nYour timezone: {}".format(from_number, tz.numberToTimeZone()))
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
