import os
import gspread
import datetime
import json
from flask import request, jsonify, url_for
from flask import Response
from twilio.twiml.voice_response import VoiceResponse, Dial, Gather, Say, Client
from twilio.rest import Client as Client
from oauth2client.service_account import ServiceAccountCredentials
from flaskapp.core.ivr_core import (google_search, save_new_user, save_data,
                                    check_new_user, update_reminder)
from flaskapp.models.ivr_model import Patient, SmartReminder, Reminder, conn
from flaskapp.tools.util import (send_mail, matchFromDf, TimeZoneHelper,
                                 getTemporaryUserData, get_txt_from_url
                                 )

from flaskapp.settings import (ORDINAL_NUMBERS, TWILIO_OPT_PHONE_NUMBER,
                               GOOGLE_SA_JSON_PATH)


def voice_joined():
    """ Function for making joined call """
    resp = VoiceResponse()
    tel = request.form['From']
    answer = request.form['SpeechResult']
    if 'Yes' in answer:
        save_new_user(tel, 'Existing')
        resp.say('Thanks for joining us. \n'
                 'We are glad to welcome you to our social network. \n'
                 'Heart Voices is a unique platform where you can make friends with the same interests.\n'
                 'With us, you can use Google search through your phone. \n'
                 'You can take advantage of the unique smart reminder feature. \n'
                 'Our system will remind you every day of important events for you, it can be a daily medication intake, the need to do something, or a reminder that you really want to learn a new language.\n'
                 'At your request, we will remind you to measure blood pressure or blood sugar, and we will collect this data for you. You can use them when you visit your doctor if needed. \n'
                 'We provide social support through friendly calls to friends and our operators. \n'
                 'After forwarding call you will access to our community.')
        resp.dial(TWILIO_OPT_PHONE_NUMBER)
    else:
        resp.say(f'We got your answer {answer}. We hope you will back us later. Take care.')
        resp.hangup()
    return (str(resp))


def voice():
    """ Function for answering from any call to Main Number of the IVR """
    resp = VoiceResponse()
    tel = request.values['From']
    user = check_new_user(tel)
    if user == 'Exist':
        resp.dial(TWILIO_OPT_PHONE_NUMBER)
    else:
        save_new_user(tel, 'Calls')
        gather = Gather(input='speech dtmf', action='/voice_joined', timeout=3, num_digits=1)
        gather.say(
            'Welcome to Heart Voices ! We help people change their habits on their way to a healthy life without heart disease. Do you want to join us? Say yes or no.')
        resp.append(gather)
    return str(resp)


def after_call():
    """ Function for saving data after call to spreadsheet """
    resp = VoiceResponse()
    req = request.values
    for r in req:
        save_data(r, req.get(r), req.get('phone'))
    return str(resp)


def username():
    """ Function for getting Name of the Client from google spreadsheet """
    req = request.values
    phone = req.get('phone')

    # GET username from SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SA_JSON_PATH, scope)
    client = gspread.authorize(creds)

    spreadsheetName = "Users"
    sheetName = "Existing"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    rows = sheet.get_all_records()
    x = {}
    for row in rows:
        tel = row.get('Phone Number')
        if phone == f'+{tel}':
            x = {"username": row.get('username')}
    return (jsonify(x))


def check_client_type():
    """ Function for checking Type of the Client from google spreadsheet (Client, Volunteer,Client and Volunteer, QA Engineer """
    req = request.values
    phone = req.get('phone')

    # GET username from SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SA_JSON_PATH, scope)
    client = gspread.authorize(creds)

    spreadsheetName = "Users"
    sheetName = "Existing"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    rows = sheet.get_all_records()
    x = {}
    for row in rows:
        tel = row.get('Phone Number')
        if phone == f'+{tel}':
            x = {"type": row.get('type')}
    return (jsonify(x))


def save_client_type():
    """ Function for checking Type of the Client from google spreadsheet (Client, Volunteer,Client and Volunteer, QA Engineer """
    resp = VoiceResponse()
    req = request.values
    save_data('type', req.get('client_type'), req.get('phone'))
    return str(resp)


def call_to_friend():
    """ Function for making call to the friend according data in the spreadsheet """

    req = request.values
    phone = req.get('phone')

    # GET username from SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SA_JSON_PATH, scope)
    client = gspread.authorize(creds)

    spreadsheetName = "Users"
    sheetName = "Existing"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    rows = sheet.get_all_records()
    x = {}
    for row in rows:
        tel = row.get('Phone Number')
        if phone == f'+{tel}':
            x = {f"friend": row.get('friend')}
    return (jsonify(x))


def find_friend_timezone():
    """Selects a match from Google sheet and connects User to friend"""
    # Start our TwiML response
    resp = VoiceResponse()
    to_number = request.form['To']
    from_number = request.form['From']  # tel = request.values['From']

    # timezone helper class to get time zone from number
    tz_from = TimeZoneHelper(from_number)

    # how to get match from temporary google sheet
    dataframe = getTemporaryUserData()
    match = matchFromDf(dataframe, tz_from)

    # now that we have match, forward call to match
    formatMatch = "+" + str(match)
    resp.say(
        "Connecting you to a friend. Please stay on the line."
    )
    resp.dial(formatMatch, action=url_for('.end_call'))  # requires "action" route to be routed to when call ends
    return Response(str(resp), 200, mimetype="application/xml")


def end_call():
    """Thank user & hang up."""
    response = VoiceResponse()
    response.say(
        "Thank you for using the Heart Voices IVR System! " + "Your voice makes a difference. Goodbye."
    )
    response.hangup()
    return Response(str(response), 200, mimetype="application/xml")


def call_to_operator():
    """ Function for making call to the operator according data in the spreadsheet """

    req = request.values
    phone = req.get('phone')

    # GET username from SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SA_JSON_PATH, scope)
    client = gspread.authorize(creds)

    spreadsheetName = "Users"
    sheetName = "Existing"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    rows = sheet.get_all_records()
    x = {}
    for row in rows:
        tel = row.get('Phone Number')
        if phone == f'+{tel}':
            x = {'operator': row.get('operator')}
    return jsonify(x)


def save_blood_pressure():
    """ Function for saving measurement of the blood pressure to the spreadsheet """
    resp = VoiceResponse()

    req = request.values
    phone = req.get('phone')
    UP = ''.join(e for e in req.get('UP') if e.isalnum())
    DOWN = ''.join(e for e in req.get('DOWN') if e.isalnum())

    # GET username from SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SA_JSON_PATH, scope)
    client = gspread.authorize(creds)
    spreadsheetName = "health_metrics"
    sheetName = "blood_pressure"
    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    new_row = [phone, UP, DOWN, json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)]
    sheet.append_row(new_row)

    return str(resp)


def save_feedback_service():
    """ Function for gathering feedback and put information about it to google spreadsheet """
    resp = VoiceResponse()
    req = request.values

    phone = ''
    REurl = 'YES'
    if req.get('phone'):
        phone = req.get('phone')
    else:
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        call = client.calls(req.get('CallSid')).fetch()
        phone = call.from_
        REurl = req.get('RecordingUrl')

    # GET username from SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SA_JSON_PATH, scope)
    client = gspread.authorize(creds)
    spreadsheetName = "feedback"
    sheetName = "service"
    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    new_row = [json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), phone, REurl]
    sheet.append_row(new_row)
    send_mail("FEEDBACK", phone=phone, feedback=REurl)

    return str(resp)


def save_feedback():
    """ Function for saving feedback and to the google spreadsheet """
    try:
        # GET username from SPREDASHEET
        phone = request.args.get('phone')
        msg = request.args.get('msg')
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SA_JSON_PATH, scope)
        client = gspread.authorize(creds)
        spreadsheetName = "feedback"
        sheetName = "service"
        spreadsheet = client.open(spreadsheetName)
        sheet = spreadsheet.worksheet(sheetName)

        new_row = [json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), phone, msg]
        sheet.append_row(new_row)
        send_mail("FEEDBACK", phone=phone, feedback=msg)
    except:
        return ('-1')
    return ('0')


def search_via_google():
    """ Prepare search results on the term provided by client

    The function performs searching using Google Custom Search Engine,
    returns #<GOOGLE_CSE_MAX_NUM> search items (see settings file)
    and prepare the result for retrieving to an user.

    Result is presented as a Flask's Response object
    with the application/json mimetype.

    """

    req = request.values
    req_str = req.get('str')
    results = google_search(req_str)

    output = '\n'.join(
        [f'{ORDINAL_NUMBERS[it]}. result: "{res}"'
         for it, res in enumerate(results)]
    )

    return jsonify({"search_result": output})


def get_next_reminder():
    req = request.values
    phone = req.get('phone')
    tel = str(phone[1:15])  # exclude +

    # conn.connect()
    # get Patient ID by the phone
    pat = Patient.get(Patient.phone == tel)
    print(pat.id, pat.phone)

    # get SmartReminders by Patient ID
    # smr = SmartReminder.get(SmartReminder.id==pat.id)
    query = SmartReminder.select().where(SmartReminder.patient_id == pat.id).order_by(SmartReminder.next_time).limit(1)
    smr_selected = query.dicts().execute()

    result = ''
    # get reminder text by SmartReminder ID
    for s in smr_selected:
        rm = Reminder.get(Reminder.id == s['reminder_id'])
        result = rm.text
        print(rm.text)
        # change next time of reminding
        update_reminder(s['reminder_id'])
        conn.commit()
    conn.close()
    return jsonify(
        {
            "text":
            f' Lets listen interesting fact of the day...{result} ...Thank you.'
        }
    )


def get_term_cond():
    return get_txt_from_url('https://www.iubenda.com/terms-and-conditions/86762295')


def get_privacy():
    return get_txt_from_url('https://www.iubenda.com/privacy-policy/86762295/full-legal')


def get_profile():
    req = request.json
    phone = req.get("Phone Number")
    pat = Patient.get(Patient.phone == phone)
    print(pat.id, pat.phone)
    patient = dict()
    patient["Phone Number"] = pat.phone
    patient["time zone"] = pat.timezone
    patient["call time"] = str(pat.callstart)
    patient["username"] = pat.username
    patient["type"] = pat.type
    print(patient)
    return jsonify(patient)
