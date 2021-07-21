"""
IVR API

This API uses for specific functions during phone call between Client and IVR system

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
import os
from flask import Flask, request, jsonify, url_for
from flask import Response
from twilio.twiml.voice_response import VoiceResponse, Dial, Gather, Say, Client
from twilio.rest import Client as Client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#from twilio.rest import Client
import time
import datetime
import json
from peewee import *
from supermemo2 import SMTwo
from util import *

cred_json = os.environ['json_path']
lst_num = ['first', 'second', 'third', 'forth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']
main_number = os.environ['main_number']
optional_number = os.environ['optional_number']
postgreSQLpass = os.environ['postgreSQLpass']

from googleapiclient.discovery import build
#import pprint

my_api_key = os.environ['google_api_key']
my_cse_id = os.environ['google_cse_id']

db_proxy = Proxy()
# Base model for work with Database through ORM
class BaseModel(Model):
    class Meta:
        database = db_proxy  # connection with database

# Patient model
class Patient(BaseModel):
    id = AutoField(column_name='ID')
    phone = TextField(column_name='phone', null=True)
    username = TextField(column_name='username', null=True)
    gender = TextField(column_name='gender', null=True)
    timezone = TextField(column_name='timezone', null=True)
    callstart = TimeField(column_name='callstart', null=True)
    callend = TimeField(column_name='callend', null=True)
    type = TextField(column_name='type', null=True)
    created = DateTimeField(column_name='created', null=True)
    updated = DateTimeField(column_name='updated', null=True)

    class Meta:
        table_name = 'patient'

# Reminder
class Reminder(BaseModel):
    id = AutoField(column_name='ID')
    text = TextField(column_name='text', null=True)

    class Meta:
        table_name = 'reminder'

# Smart Reminder
class SmartReminder(BaseModel):
    id = AutoField(column_name='ID')
    patient_id = IntegerField(column_name='patientid')
    reminder_id = IntegerField(column_name='reminderid')

    easiness = FloatField(column_name='easiness', null=True)
    interval = IntegerField(column_name='interval', null=True)
    repetitions = IntegerField(column_name='repetitions', null=True)

    last_time = DateTimeField(column_name='lasttime', null=True)
    next_time = DateTimeField(column_name='nexttime', null=True)

    class Meta:
        table_name = 'smartreminder'
if 'HEROKU' in os.environ:
    import urllib.parse
    import psycopg2
    urllib.parse.uses_netloc.append('postgres')
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    conn = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
    db_proxy.initialize(conn)
else:
    conn = PostgresqlDatabase('goanddo', user='postgres', password=postgreSQLpass, host='127.0.0.1', port=5432)
    db_proxy.initialize(conn)


def out_bound_call (tel):
    """ Function for making outbound call"""
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    status = check_new_user(tel)
    if (status != 'New'):
        execution = client.studio \
            .flows('FW66222e22d7301b1f1e0f02ca198c440a') \
            .executions \
            .create(to=tel, from_=main_number)
    else:
        execution = client.studio \
            .flows('FW21a0b56a4c5d0d9635f9f86616036b9c') \
            .executions \
            .create(to=tel, from_=main_number)
def call_flow(flow_sid, tel=''):
    """ Function for calling any flow from Twilio Studion """
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    if tel != '':
        status = check_new_user(tel)
        if (status != 'New'):
            print (f'start call for existing User {tel}')
            execution = client.studio \
                .flows(flow_sid) \
                .executions \
                .create(to=tel, from_=main_number)
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
                .create(to=tel, from_=main_number)


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
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
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
        .create(to='+16692419870', from_=main_number)

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
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    client = gspread.authorize(creds)

    new_row = [json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), UP, DOWN]
    spreadsheetName = "Ekaterina"
    sheetName = "Blood_Preassure"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    sheet.append_row(new_row)
    time.sleep(5)
def check_new_user(tel=''):
    """ Function for checking type of User (NEW/EXISTING) """
    # check data in spreadsheet
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    client = gspread.authorize(creds)

    spreadsheetName = "Users"
    sheetName = "Existing"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)
    all_sheet = sheet.get_all_values()
    phone_lst = []
    for a in all_sheet:phone_lst.append(a[0])
    tel_not_plus = str(tel[1:15])
    if tel_not_plus in phone_lst:
        return 'Exist'
    else:
        return 'New'
app = Flask(__name__)

def save_new_user(tel='', tab=''):
    """ Function for saving NEW user in google spreadsheet"""
    # check data in spreadsheet
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    client = gspread.authorize(creds)

    spreadsheetName = 'Users'
    sheetName = tab

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    new_row = [tel[1:15],'','','','','','','','','','','',json.dumps(datetime.datetime.now(),indent=4, sort_keys=True, default=str),'19258609793','19258609793']
    sheet.append_row(new_row)
    send_mail("NEW USER", phone=tel)
@app.route("/voice_joined", methods=['GET', 'POST'])
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
        resp.dial(optional_number)
    else:
        resp.say(f'We got your answer {answer}. We hope you will back us later. Take care.')
        resp.hangup()
    return(str(resp))
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """ Function for answering from any call to Main Number of the IVR """
    resp = VoiceResponse()
    tel = request.values['From']
    user = check_new_user(tel)
    if user == 'Exist':resp.dial(optional_number)
    else:
        save_new_user(tel,'Calls')
        gather = Gather(input='speech dtmf', action='/voice_joined',  timeout=3, num_digits=1)
        gather.say('Welcome to Heart Voices ! We are really helping to people in their journey to a healthy life. Do you want to join us? Say yes or no.')
        resp.append(gather)
    return str(resp)
def save_data(col_name, value, tel):
    """ Function for saving data to google spreadsheet """
    # PUT DATA TO SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
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
@app.route("/after_call", methods=['GET', 'POST'])
def after_call():
    """ Function for saving data after call to spreadsheet """
    resp = VoiceResponse()
    req = request.values
    for r in req:
        save_data(r, req.get(r), req.get('phone'))
    return str(resp)
@app.route("/username", methods=['GET', 'POST'])
def username():
    """ Function for getting Name of the Client from google spreadsheet """
    req = request.values
    phone = req.get('phone')

    # GET username from SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    client = gspread.authorize(creds)

    spreadsheetName = "Users"
    sheetName = "Existing"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    all_sheet = sheet.get_all_values()
    rows = sheet.get_all_records()
    x = {}
    for row in rows:
        tel = row.get('Phone Number')
        if phone == f'+{tel}':
            x = {"username": row.get('username')}
    return (jsonify(x))
@app.route("/check_client_type", methods=['GET', 'POST'])
def check_client_type():
    """ Function for checking Type of the Client from google spreadsheet (Client, Volunteer,Client and Volunteer, QA Engineer """
    req = request.values
    phone = req.get('phone')

    # GET username from SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    client = gspread.authorize(creds)

    spreadsheetName = "Users"
    sheetName = "Existing"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    all_sheet = sheet.get_all_values()
    rows = sheet.get_all_records()
    x = {}
    for row in rows:
        tel = row.get('Phone Number')
        if phone == f'+{tel}':
            x = {"type": row.get('type')}
    return (jsonify(x))
@app.route("/save_client_type", methods=['GET', 'POST'])
def save_client_type():
    """ Function for checking Type of the Client from google spreadsheet (Client, Volunteer,Client and Volunteer, QA Engineer """
    resp = VoiceResponse()
    req = request.values
    save_data('type', req.get('client_type'), req.get('phone'))
    return str(resp)

@app.route("/call_to_friend", methods=['GET', 'POST'])
def call_to_friend():
    """ Function for making call to the friend according data in the spreadsheet """
    resp = VoiceResponse()

    req = request.values
    phone = req.get('phone')

    # GET username from SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
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

@app.route("/find_friend_timezone", methods=['GET', 'POST'])
def find_friend_timezone():
    """Selects a match from Google sheet and connects User to friend"""
    # Start our TwiML response
    resp = VoiceResponse()
    to_number = request.form['To']
    from_number = request.form['From']  #tel = request.values['From']
    
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
    resp.dial(formatMatch, action=url_for('.end_call')) # requires "action" route to be routed to when call ends
    return Response(str(resp), 200, mimetype="application/xml")

@app.route('/end_call', methods=['GET', 'POST'])
def end_call():
    """Thank user & hang up."""
    response = VoiceResponse()
    response.say(
        "Thank you for using the Heart Voices IVR System! " + "Your voice makes a difference. Goodbye."
    )
    response.hangup()
    return Response(str(response), 200, mimetype="application/xml")

@app.route("/call_to_operator", methods=['GET', 'POST'])
def call_to_operator():
    """ Function for making call to the operator according data in the spreadsheet """
    resp = VoiceResponse()

    req = request.values
    phone = req.get('phone')

    # GET username from SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
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
    return (jsonify(x))

@app.route("/save_blood_pressure", methods=['GET', 'POST'])
def save_blood_pressure():
    """ Function for saving measurement of the blood pressure to the spreadsheet """
    resp = VoiceResponse()

    req = request.values
    phone = req.get('phone')
    UP = ''.join(e for e in req.get('UP') if e.isalnum())
    DOWN = ''.join(e for e in req.get('DOWN') if e.isalnum())

    # GET username from SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    client = gspread.authorize(creds)
    spreadsheetName = "health_metrics"
    sheetName = "blood_pressure"
    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    new_row = [phone, UP, DOWN, json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)]
    sheet.append_row(new_row)

    return(str(resp))

@app.route("/save_feedback_service", methods=['GET', 'POST'])
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
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    client = gspread.authorize(creds)
    spreadsheetName = "feedback"
    sheetName = "service"
    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    new_row = [json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), phone, REurl]
    sheet.append_row(new_row)
    send_mail("FEEDBACK", phone=phone, feedback=REurl)

    return (str(resp))
@app.route("/save_feedback", methods=['GET', 'POST'])
def save_feedback():
    """ Function for saving feedback and to the google spreadsheet """
    try:
        # GET username from SPREDASHEET
        phone = request.args.get('phone')
        msg = request.args.get('msg')
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
        client = gspread.authorize(creds)
        spreadsheetName = "feedback"
        sheetName = "service"
        spreadsheet = client.open(spreadsheetName)
        sheet = spreadsheet.worksheet(sheetName)

        new_row = [json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), phone, msg]
        sheet.append_row(new_row)
        send_mail("FEEDBACK", phone=phone, feedback=msg)
    except:
        return('-1')
    return ('0')
def google_search(search_term, api_key, cse_id, **kwargs):
    """ Function for using Google Search API"""
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']
@app.route("/search", methods=['GET', 'POST'])
def search():
    """ Function for answering search results on phrase from Client"""
    req = request.values
    req_str = req.get('str')

    results = google_search(req_str, my_api_key, my_cse_id, num=10)
    it = 0
    str = ''
    for result in results:
        #title=result.get('title')
        res=result.get('snippet')
        #name = result.get('displayLink')
        str= str + f'{lst_num[it]} result: {res}".\n'
        it=it+1
        if it == 3: break
    x = {"search_result": str}
    return (jsonify(x))
# def print_mars_photos():
#     from redis import Redis
#     from rq import Queue
#
#     from mars import get_mars_photo
#
#     q = Queue(connection=Redis())
#
#     print('Before')
#     for i in range(10):
#         #get_mars_photo(1 + i)
#         q.enqueue(get_mars_photo, 1 + i)
#     print('After')
#print_mars_photos()

def db_create_tables():
    conn.drop_tables([Patient, Reminder, SmartReminder])
    # conn.cursor().execute("drop table patient")
    # conn.cursor().execute("drop table reminder")
    # conn.cursor().execute("drop table smartreminder")

    conn.create_tables([Patient, Reminder, SmartReminder])
    conn.commit()

    conn.cursor().execute("INSERT INTO Patient(Phone, Username, Gender, Timezone, CallStart,CallEnd, Type, Created, Updated) VALUES ('13333333333', 'Alex', 'Male', 'Pacific Standard Time', '16:00:00', '18:00:00', 'Volunteer', now(), now())")
    conn.cursor().execute("INSERT INTO Patient (Phone, Username, Gender, Timezone, CallStart,CallEnd, Type, Created, Updated) VALUES ('12222222222', 'Lina', 'Male', 'Pacific Standard Time', '16:00:00', '18:00:00', 'Volunteer', now(), now())")
    conn.cursor().execute("INSERT INTO Reminder (Text) VALUES ('Get at least 150 minutes per week of moderate-intensity aerobic activity or 75 minutes per week of vigorous aerobic activity, or a combination of both, preferably spread throughout the week.')")
    conn.cursor().execute("INSERT INTO Reminder (Text) VALUES ( 'Add moderate- to high-intensity muscle-strengthening activity (such as resistance or weights) on at least 2 days per week.')")
    conn.cursor().execute("INSERT INTO Reminder (Text) VALUES ( 'Spend less time sitting. Even light-intensity activity can offset some of the risks of being sedentary.')")
    conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('1', '1', now())")
    conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('1', '2', now())")
    conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('1', '3', now())")
    conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('2', '1', now())")
    conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('2', '2', now())")
    conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('2', '3', now())")

    conn.commit()
    #conn.close()
@app.route("/get_next_reminder", methods=['GET', 'POST'])
def get_next_reminder():
    req = request.values
    phone = req.get('phone')
    tel = str(phone[1:15]) # exclude +

    #conn.connect()
    # get Patient ID by the phone
    pat = Patient.get(Patient.phone == tel)
    print(pat.id, pat.phone)

    # get SmartReminders by Patient ID
    #smr = SmartReminder.get(SmartReminder.id==pat.id)
    query = SmartReminder.select().where(SmartReminder.patient_id == pat.id).order_by(SmartReminder.next_time).limit(1)
    smr_selected = query.dicts().execute()

    result = ''
    # get reminder text by SmartReminder ID
    for s in smr_selected:
        rm = Reminder.get(Reminder.id==s['reminder_id'])
        result = rm.text
        print (rm.text)
        # change next time of reminding
        update_reminder(s['reminder_id'])
        conn.commit()
    conn.close()
    x = {"text":f' Lets listen interesting fact of the day...{result} ...Thank you.'}
    return (jsonify(x))
def init_db():
    with conn.atomic() as transaction:  # Opens new transaction.
        try:
            db_create_tables()
            print ("tables in database created...")
        except:
            # Because this block of code is wrapped with "atomic", a
            # new transaction will begin automatically after the call
            # to rollback().
            transaction.rollback()
            print ("rollback ...")
            error_saving = True
            raise

        #create_report(error_saving=error_saving)
        # Note: no need to call commit. Since this marks the end of the
        # wrapped block of code, the `atomic` context manager will
        # automatically call commit for us.
    conn.close()
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

    # second review
    # review = SMTwo(r.easiness, r.interval, r.repetitions).review(level, r.review_date)
    # print(r.review_date, review)
    # dt = r.review_date
    # for i in range(10):
    #     dt = dt + datetime.timedelta(days=1)
    #     review = SMTwo(review.easiness, review.interval, review.repetitions).review(level, dt)
    #     print(dt, review)
if __name__ == '__main__':
    print ('start db connect...')
    db_proxy.connect()
    #db_proxy.create_tables([Patient, Reminder, SmartReminder], safe=True)
    print('init db...')
    init_db()
    app.run(debug=True)
