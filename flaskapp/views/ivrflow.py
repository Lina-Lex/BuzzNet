#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
This file is a part of heartvoices.org project.

The software embedded in or related to heartvoices.org
is provided under a some-rights-reserved license. This means
that Users are granted broad rights, including but not limited
to the rights to use, execute, copy or distribute the software,
to the extent determined by such license. The terms of such
license shall always prevail upon conflicting, divergent or
inconsistent provisions of these Terms. In particular, heartvoices.org
and/or the software thereto related are provided under a GNU GPLv3 license,
allowing Users to access and use the software’s source code.
Terms and conditions: https://www.goandtodo.org/terms-and-conditions

Created Date: Sunday September 26th 2021
Author: GO and to DO Inc
E-mail: heartvoices.org@gmail.com
-----
Last Modified: Sunday, November 7th 2021, 1:40:29 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""
import logging
import os
import gspread
import datetime
import json
from flask import request, jsonify, url_for
from flask import Response
from sqlalchemy.orm import join
from twilio.twiml.voice_response import VoiceResponse, Dial, Gather, Say
from twilio.rest import Client
from oauth2client.service_account import ServiceAccountCredentials
from flaskapp.views.authenticate import is_user_authenticated
from playhouse.shortcuts import model_to_dict
from flaskapp.core.ivr_core import (google_search, save_new_user, save_data,
                                    is_user_new, update_reminder)
from flaskapp.models.ivr_models import PhoneNumber, User, SmartReminder, Reminder, HealthMetric, Call
from flaskapp.tools.utils import (send_mail, matchFromDf, TimeZoneHelper,
                                  getTemporaryUserData, get_txt_from_url,
                                  cleanup_phone_number)
from flaskapp.models.storages import gs_users_existing, gs_health_metric_data

from flaskapp.settings import (ORDINAL_NUMBERS, TWILIO_OPT_PHONE_NUMBER,
                               GOOGLE_SA_JSON_PATH, TWILIO_MAIN_PHONE_NUMBER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN,
                               MAGIC_NUMBER)
from flaskapp.dialogs import THANKS_FOR_JOIN, WELCOME_GREETING, GOOD_BYE

try:
    from functools import cache
except ImportError:
    from functools import lru_cache

    cache = lru_cache(maxsize=None)


def voice_joined():
    """ Function for making joined call """
    voice_response = VoiceResponse()
    phone_number = request.form['From']
    username = request.form['Caller']
    answer = request.form['SpeechResult'].lower().strip()
    if 'yes' in answer:
        save_new_user(username, phone_number, 'Existing')
        voice_response.say(THANKS_FOR_JOIN)
        voice_response.dial(TWILIO_OPT_PHONE_NUMBER)
    else:
        voice_response.say(f"We got your answer {answer}."
                           "We hope you will back us later. Take care.")
        voice_response.hangup()
    return str(voice_response)


def voice():
    """ Function for answering from any call to Main Number of the IVR """

    voice_response = VoiceResponse()
    phone_number = request.values['From']
    username = request.values['Caller']
    if not is_user_new(phone_number):
        voice_response.dial(TWILIO_OPT_PHONE_NUMBER)
    else:
        save_new_user(username, phone_number, 'Calls')
        gather = Gather(input='speech dtmf',
                        action='/voice_joined', timeout=3, num_digits=1)
        gather.say(WELCOME_GREETING)
        voice_response.append(gather)
    return str(voice_response)


def after_call():
    """ Function for saving data after call to spreadsheet """

    voice_response = VoiceResponse()
    request_values = request.values
    current_date = datetime.datetime.now()
    phone_number = cleanup_phone_number(request_values.get('phone'))
    for key, val in request_values.items():
        save_data(key, val, phone_number, date=current_date)
    return str(voice_response)


def get_username():
    """ Function for getting Name of the Client from google spreadsheet """

    request_values = request.values
    phone_number = cleanup_phone_number(request_values.get('phone'))
    # TODO: gs-support should be dropped
    rows = gs_users_existing.get_all_records()
    for row in rows:
        # FIXME: WE have different names 'phone' and 'Phone Number' (bad)
        tel = cleanup_phone_number(str(row.get('Phone Number')))
        if phone_number == tel:
            x = {"username": row.get('username')}

    user_query = User.select().join(PhoneNumber).where(
        PhoneNumber.number == phone_number
    )
    user = lambda z: z[0].username if len(z) != 0 else None

    # FIXME: data from postgres have precedence
    # should be removed when gs-support will be dropped
    return jsonify({"username": user(user_query)} or x)


def get_client_type():
    """ Function for checking Type of the Client from google spreadsheet
    (Client, Volunteer, Client and Volunteer, QA Engineer
    """
    request_values = request.values
    phone_number = cleanup_phone_number(request_values.get('phone'))
    # TODO: gs-support should be dropped
    rows = gs_users_existing.get_all_records()
    for row in rows:
        # FIXME: WE have different names 'phone' and 'Phone Number' (bad)
        tel = cleanup_phone_number(str(row.get('Phone Number')))
        if phone_number == tel:
            x = {"type": row.get('type')}

    query = User.select().join(PhoneNumber, on=(User.id == PhoneNumber.user)).where(
        PhoneNumber.number == phone_number
    )

    # FIXME: should be changed when gs-support will be dropped
    user = lambda z: z[0].type if len(z) != 0 else None
    return jsonify({"type": user(query)} or x)


def save_client_type():
    """Function for saving client type to google
    spreadsheet and postgres

    Client Types: Client, Volunteer,Client and Volunteer, QA Engineer

    :return: VoiceReponse instance (empty xml-like document)
    :rtype: str
    """
    voice_response = VoiceResponse()
    request_values = request.values
    date = datetime.datetime.now()

    save_data(
        'type',
        request_values.get('client_type'),
        request_values.get('phone'),
        date=date
    )

    return str(voice_response)


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
    response.say(GOOD_BYE)
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
    tel = cleanup_phone_number(phone)  # exclude +

    query = User.select() \
        .join(PhoneNumber, on=(User.id == PhoneNumber.user)) \
        .where(PhoneNumber.number == tel)

    user = query[0]

    # get SmartReminders by User ID
    smr_selected = SmartReminder.select().where(SmartReminder.user == user.id).order_by(SmartReminder.next_time).limit(
        1)
    print(smr_selected)
    result = ''
    # get reminder text by SmartReminder ID
    for s in smr_selected:
        print(s)
        rm = Reminder.get(Reminder.id == s.reminder_id)
        result = rm.text
        print(rm.text)
        # change next time of reminding
        update_reminder(s.reminder_id)

    return jsonify(
        {
            "text":
                f' Lets listen interesting fact of the day...{result} ...Thank you.'
        }
    )


@cache
def get_term_cond():
    """ Returns terms and conditions represented as Flask response object """
    return get_txt_from_url('https://www.iubenda.com/terms-and-conditions/86762295')


@cache
def get_privacy():
    """ Returns Privacy-policy document represented as Flask response object """
    return get_txt_from_url('https://www.iubenda.com/privacy-policy/86762295/full-legal')


def get_profile():
    req = request.json
    phone = req.get("Phone Number")
    tel = cleanup_phone_number(phone)
    print(tel)
    auth, message = is_user_authenticated(phone)
    print(auth, message)
    if auth:
        user = User.select(User, PhoneNumber, Call) \
            .join(PhoneNumber, on=(User.id == PhoneNumber.user)) \
            .join(Call, on=(User.id == Call.user)) \
            .where(PhoneNumber.number == tel)

        print(user.get())

        patient = dict()
        for pat in user:
            print(pat)

            patient["Phone Number"] = pat.phonenumber.number
            patient["time zone"] = pat.timezone
            patient["call time"] = str(pat.phonenumber.call.call_start)
            patient["username"] = pat.username
            patient["type"] = pat.type
            print(patient)

        return jsonify(patient)
    else:
        return message


# http://127.0.0.1:5000/new_user?username=testuser&&type=patient&&timezone=US/Pacific&&calltime=5:30:00&&phone=123-456-789
def new_user():
    all_args = request.args.to_dict()
    rec1 = User.create(**all_args)
    rec1.save()
    return {"success": 200, "newuser": model_to_dict(rec1)}


def unsubscribe():
    user_info = request.args.to_dict()
    ph = user_info.get('phone')
    del_row = User.delete().where(User.phone == ph)
    if del_row > 0:
        return {"success": 200, "message": "user unsubscribed"}
    return {"message": "user not found", "failed": 400}


# getting set of from_ numbers from twilio call logs  that are less than 7 days old
def get_from_phone_number_from_twilio_call_logs():
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    start = datetime.datetime.now()
    calls = [call.from_ for call in client.calls.list() if
             (start.date() - call.start_time.date()) <= datetime.timedelta(days=MAGIC_NUMBER)
             and TWILIO_MAIN_PHONE_NUMBER != call.from_]

    return set(calls)


# getting healthMetric data by days interval for a particular patient or user
def get_data_by_days_interval():
    req = request.values
    phone = cleanup_phone_number(req.get('phone'))
    days = int(req.get('days'))
    query = HealthMetric.select() \
        .join(PhoneNumber, on=(HealthMetric.user == PhoneNumber.user)) \
        .where(PhoneNumber.number == phone)
    list_of_data = list()
    for item in query:
        data = {}
        duration = datetime.datetime.now() - datetime.datetime.fromisoformat(item.data["DateTime"])
        if duration <= datetime.timedelta(days=days):
            data['UP'] = item.data['UP']
            data['DOWN'] = item.data['DOWN']
            data['DateTime'] = item.data['DateTime']
            list_of_data.append(data)

    return jsonify(list_of_data)
