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
Last Modified: Sunday, October 3rd 2021, 5:07:42 pm
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import datetime
from flask import jsonify
import pandas as pd
from pytz import timezone
import phonenumbers
from phonenumbers import geocoder
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client
from flaskapp.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

recipient_list = ['goandtodo@googlegroups.com']

sender_mail = 'heartvoices.org@gmail.com'


def send_mail(mail_type, phone, feedback=''):
    """
    Function is used for sending the mail when the user is created and the user gives feedback
    the type of the mail is decided by mail_type of the argument.
    """
    phone = str(phone[0:5] + '*****' + phone[10:])
    if mail_type == 'FEEDBACK':
        with open('templates/feedback.html', 'r') as template:
            html = ''.join(template.readlines())
            message = Mail(
                from_email=sender_mail,
                to_emails=recipient_list,
                subject=mail_type,
                html_content=html.format(phone=phone, feedback=feedback))

    elif mail_type == 'NEW USER':
        with open('templates/welcome.html', 'r') as template:
            html = ''.join(template.readlines())
            message = Mail(
                from_email=sender_mail,
                to_emails=recipient_list,
                subject=mail_type,
                html_content=html.format(phone=phone))
    else:
        print("Please check the mail_type before sending mail")
        return
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        if response.status_code == 202:
            print('send successfully')
    except Exception as e:
        print(e)


# helper class
class TimeZoneHelper:
    def __init__(self, phoneNumber):
        self.phoneNumber = phoneNumber
        self.tzs_df = pd.read_csv("data/tzmapping.csv")
        self.tzs_df.index = self.tzs_df['State']
        self.user_zone = self.numberToTimeZone()
        self.fmt = '%Y-%m-%d %H:%M:%S %Z%z'

    def numberToTimeZone(self):
        """This function converts a phone number to a timezone"""
        fmtNum = phonenumbers.parse("+" + str(self.phoneNumber))
        state = geocoder.description_for_number(fmtNum, 'en')
        time_zone = self.tzs_df.loc[state]['Zone'].split(" ")[0]
        return "US/" + time_zone

    def utcToLocal(self):
        """This function gets current local time from utc time given a zone in 24-hour time format"""
        # get utc time
        utc_dt = datetime.datetime.utcnow()
        # convert to localtime using tz object and string formatter
        zone_objct = timezone(self.user_zone)
        loc_dt = utc_dt.astimezone(zone_objct)
        return loc_dt.strftime(self.fmt)


# helper function to get temporary User data
def getTemporaryUserData():
    """This function gets temporary data from google sheet with proper formatting of User data"""
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('data/master_key.json', scope)
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1M-IQ-iYji-dbJSkrPehh3CMLiLGlzWZBzzGqVWzJPog/edit?usp=sharing")
    # get all worksheets
    sheet_instance = sheet.worksheets()
    # convert to dataframe
    dataframe = pd.DataFrame(sheet_instance[0].get_all_records())
    return dataframe


# helper function to find appropriate match from temporary User data
def matchFromDf(dataframe, tz_from, verbose=False):
    """This function gets a match for user to call"""
    df = dataframe
    df[["DT Start"]] = df[["UTC start"]].apply(pd.to_datetime)
    df[["DT End"]] = df[["UTC end"]].apply(pd.to_datetime)

    # get current UTC time and find match
    now_utc = datetime.datetime.utcnow()
    tz = tz_from.numberToTimeZone()  # tz = "US/Pacific"
    mask = (df['DT Start'] < now_utc) & (df['DT End'] >= now_utc) & (df['time zone'] == tz)
    result = df.loc[mask]
    match = result.head(1)
    match = int(match['Number'])

    # log to console if necessary (default=False)
    if verbose:
        print(f"dataframe shape {dataframe.shape}")  # all results shape
        print(f"result shape: {result.shape}")  # candidate matches shape

    return match


def call_duration_from_api(phone):
    """
    The function is used for fetching the call duration for a particular number from the call log API of
    twilio and sum up the duration for the day and return it.
    """
    if phone:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        date = datetime.datetime.today()
        calls = client.calls.list(from_=str(phone),
                                  start_time_after=datetime.datetime(date.year, date.month, date.day, 0, 0, 0))
        duration = 0
        for record in calls:
            duration += int(record.duration)
        return duration
    raise ValueError("No valid phone number found")


def get_txt_from_url(url):
    """Retrieve text from a given url and split it into two parts
    wrapped as Flask response object

    :param url: an url to read a text block from
    :type url: str
    :return: Flask Response object with application/json mimetype
    :rtype: Flask Response object
    """

    import urllib
    from bs4 import BeautifulSoup

    # FIXME: What if .read take a long time to get the data... , or 404?
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)
    text = soup.get_text()

    # NOTE: Do we need to define these magic numbers in the config file, e.g. 15002?
    return jsonify({"text1": text[0:15002], "text2": text[15002:30000]})