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
Last Modified: Sunday, October 3rd 2021, 6:08:34 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from oauth2client.service_account import ServiceAccountCredentials
from supermemo2 import SMTwo
import gspread
import time
import datetime
import json
from twilio.rest import Client as Client
import os
from googleapiclient.discovery import build
from flaskapp.models.storages import gs_users_existing, gs_users_calls
from flaskapp.settings import *
from flaskapp.tools.util import *
from flaskapp.models.ivr_models import *
from flaskapp.settings import (GOOGLE_API_KEY, GOOGLE_CSE_ID,
                               GOOGLE_CSE_MAX_NUM, GOOGLE_SA_JSON_PATH,
                               GOOGLE_USERS_SPREADSHEET_ID,
                               GOOGLE_USERS_SHEET_NAME_EXISTING,
                               TWILIO_MAIN_PHONE_NUMBER
                               )


def out_bound_call (tel):
    """ Function for making outbound call"""
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    if is_user_new(tel):
        execution = client.studio \
            .flows('FW66222e22d7301b1f1e0f02ca198c440a') \
            .executions \
            .create(to=tel, from_=TWILIO_MAIN_PHONE_NUMBER)
    else:
        execution = client.studio \
            .flows('FW21a0b56a4c5d0d9635f9f86616036b9c') \
            .executions \
            .create(to=tel, from_=TWILIO_MAIN_PHONE_NUMBER)
def call_flow(flow_sid, tel=''):
    """ Function for calling any flow from Twilio Studion """
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    if tel != '':
        if is_user_new(tel):
            print (f'start call for existing User {tel}')
            execution = client.studio \
                .flows(flow_sid) \
                .executions \
                .create(to=tel, from_=TWILIO_MAIN_PHONE_NUMBER)
            # wait for getting data from studio flow
            steps = client.studio.flows(flow_sid) \
                .executions(execution.sid) \
                .steps \
                .list(limit=20)
        else:
            print(f'start call for new User {tel}')
            execution = client.studio \
                .flows('FW66222e22d7301b1f1e0f02ca198c440a') \
                .executions \
                .create(to=tel, from_=TWILIO_MAIN_PHONE_NUMBER)


            # while len(steps) < 12:
            #     steps = client.studio.flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
            #         .executions(execution.sid) \
            #         .steps \
            #         .list(limit=20)
            #     time.sleep(5)
            #     print(len(steps))
            #
            # last_step_sid = steps[0].sid
            # execution_step_context = client.studio \
            #     .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
            #     .executions(execution.sid) \
            #     .steps(last_step_sid) \
            #     .step_context() \
            #     .fetch()
def profile_detail():
    """ Function for gathering profile information from the Client"""
    # check data in spreadsheet
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SA_JSON_PATH, scope)
    client = gspread.authorize(creds)
    spreadsheetName = "Users"
    sheetName = "Existing"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)
    #all_sheet = sheet.get_all_values()
    rows = sheet.get_all_records()

    row_num = 0
    for r in rows:
        ph = r.get('Phone Number')

        for v in r:
            val = r.get(v)
            if val == '':
                if v in ('dob', 'gender'):
                    print(f'getting {v} from {ph}')
                    call_flow('FWa23b5f2570ae23e2e1d68448378af0d0', str(ph))
                    break
                elif v in ('weight', 'height'):
                    print(f'getting {v} from {ph}')
                    call_flow ('FW6661af875fa71bfcc36030d653e745ec', str(ph))
                    break
                elif v in ('activity', 'hobby'):
                    print(f'getting {v} from {ph}')
                    call_flow('FW8db981daac5317452c78944626de52ac', str(ph))
                    break
                elif v in ('time zone', 'call time'):
                    print(f'getting {v} from {ph}')
                    call_flow('FWac7f7be3dcc167fed511d4c08cf76f8c', str(ph))
                    break
                elif v in ('emergency phone', 'emergency name'):
                    print(f'getting {v} from {ph}')
                    call_flow('FW21a0b56a4c5d0d9635f9f86616036b9c', str(ph))
                    break
            else:
                print(f'for {ph}:{v} is good')

def call_to_check_bld():
    """ Function for checking blood pressure and saving results to google spreadsheet """
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    # call studio flow from Python app

    execution = client.studio \
        .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
        .executions \
        .create(to='+16692419870', from_=TWILIO_MAIN_PHONE_NUMBER)

    steps = client.studio.flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
        .executions(execution.sid) \
        .steps \
        .list(limit=20)
    while len(steps) < 12:
        steps = client.studio.flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
            .executions(execution.sid) \
            .steps \
            .list(limit=20)
        time.sleep(5)
        print(len(steps))
    # sid = execution.sid
    # execution_step = client.studio \
    #                         .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
    #                         .executions('FN76531ee7fcda3617d99bec690d915045') \
    #                         .steps \
    #                         .fetch()

    # call specific Flow and Execution only for understanding and deveopment
    # execution = client.studio \
    #                   .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
    #                   .executions('FN76531ee7fcda3617d99bec690d915045') \
    #                   .fetch()

    last_step_sid = steps[0].sid
    execution_step_context = client.studio \
        .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
        .executions(execution.sid) \
        .steps(last_step_sid) \
        .step_context() \
        .fetch()

    UP = execution_step_context.context['flow']['variables'].get('UP')
    DOWN = execution_step_context.context['flow']['variables'].get('DOWN')

    # PUT DATA TO SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SA_JSON_PATH, scope)
    client = gspread.authorize(creds)

    new_row = [json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), UP, DOWN]
    spreadsheetName = "Ekaterina"
    sheetName = "Blood_Preassure"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    sheet.append_row(new_row)
    time.sleep(5)


def is_user_new(phone_number=''):
    """Check if the user already registered in the System

    :param phone_number: User's phone number, defaults to ''
    :type phone_number: str, optional
    :return: False if the user already registered and True otherwise
    :rtype: True or False
    """

    all_sheets = gs_users_existing.get_all_values()
    cleaned_phone_number = phone_number.replace('+', '').strip()
    return not any([True for a in all_sheets if cleaned_phone_number == a[0]])


def save_new_user(tel='', tab=''):
    """ Function for saving NEW user in google spreadsheet"""

    # --- store data to google spreadsheet ( TODO: drop gs support)
    gs_proxy_sheet = gs_users_existing if tab.lower() == 'existing' else gs_users_calls
    new_row = [tel[1:15],'','','','','','','','','','','',json.dumps(datetime.datetime.now(),indent=4, sort_keys=True, default=str),'19258609793','19258609793']
    gs_proxy_sheet.append_row(new_row)

    # --- store new user and related call 
    # TODO: Save new user to postgres db (implementation)

    send_mail("NEW USER", phone=tel)


def save_data(col_name, value, tel):
    """ Function for saving data to google spreadsheet """
    # PUT DATA TO SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SA_JSON_PATH, scope)
    client = gspread.authorize(creds)

    spreadsheetName = "Users"
    sheetName = "Existing"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    all_sheet = sheet.get_all_values()
    rows = sheet.get_all_records()
    row_num = 0
    for r in all_sheet:
        row_num = row_num + 1
        ph = r[0] #find the Phone Number
        if tel == f'+{ph}':
            break

    col_num = 0
    for c in all_sheet[0]:
        col_num = col_num + 1
        if col_name == c:
            print(row_num, col_num, col_name, value)
            sheet.update_cell(row_num, col_num, value)
            break


def google_search(search_term):
    """ Search a term using Google Custom Search Engine

    :param search_term: a term to search for;
    :type search_term: str

    NOTE
    ----
        see: https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
    """

    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    res = service.cse().list(
        q=search_term,
        cx=GOOGLE_CSE_ID,
        num=GOOGLE_CSE_MAX_NUM
    ).execute()
    return res.get('items', '')


def update_reminder(id):

    # get smart reminder by ID
    smr = SmartReminder.get(SmartReminder.id==id)
    #smr = SmartReminder()
    r = SMTwo.first_review(3)
    if smr.last_time is None:
        # first review
        r = SMTwo.first_review(3)
        print(r)
    else:
        # next review
        r = SMTwo(smr.easiness, smr.interval, smr.repetitions).review(3)
        print(r)
    smr.interval = r.interval
    smr.easiness = r.easiness
    smr.repetitions = r.repetitions
    smr.last_time = datetime.datetime.now()
    smr.next_time = r.review_date
    smr.save()