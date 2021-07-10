import os

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

# # Your Auth Token from twilio.com/console
# ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
# AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

def example():
    """
    Some example usage of different twilio resources.
    """
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # Get all messages
    all_messages = client.messages.list()
    print('There are {} messages in your account.'.format(len(all_messages)))

    # Get only last 10 messages...
    some_messages = client.messages.list(limit=10)
    print('Here are the last 10 messages in your account:')
    for m in some_messages:
        print(m)

    # Get messages in smaller pages...
    all_messages = client.messages.list(page_size=10)
    print('There are {} messages in your account.'.format(len(all_messages)))

    print('Sending a message...')
    new_message = client.messages.create(
    to='+19253393908',
    from_='+19252915450',
    body="Hello mate!!")

    print('Making a call...')
    new_call = client.calls.create(to='+19252915450', from_='+19253393908', method='GET', url="https://da741354f0d4.ngrok.io/voice")

    #new_call = client.calls.create(to='+19253393908', from_='+19252915450', method='GET',url="https://da741354f0d4.ngrok.io/voice")

    print('Serving TwiML')
    twiml_response = VoiceResponse()
    twiml_response.say('Hello!')
    twiml_response.hangup()
    twiml_xml = twiml_response.to_xml()
    print('Generated twiml: {}'.format(twiml_xml))


if __name__ == '__main__':
    example()
