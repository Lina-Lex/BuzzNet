import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import pandas as pd
from pytz import timezone
import phonenumbers
from phonenumbers import geocoder
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import subprocess
import datetime

recipient_list = ['goandtodo@googlegroups.com']
gmail_user = os.environ['gmail_user']
gmail_password = os.environ['gmail_password']
sender_mail = 'heartvoices.org@gmail.com'


def send_mail(mail_type, phone, feedback=''):
    """
    Function is used for sending the mail when the user is created and the user gives feedback
    the type of the mail is decided by mail_type of the argument.
    """
    phone = str(phone[0:5] + '*****' + phone[10:])
    msg = MIMEMultipart('alternative')
    msg['Subject'] = mail_type
    if mail_type == 'FEEDBACK':
        with open('templates/feedback.html', 'r') as template:
            html = ''.join(template.readlines())
            content = html.format(phone=phone, feedback=feedback)
            content = MIMEText(content, 'html')
            msg.attach(content)
    elif mail_type == 'NEW USER':
        with open('templates/welcome.html', 'r') as template:
            html = ''.join(template.readlines())
            content = html.format(phone=phone)
            content = MIMEText(content, 'html')
            msg.attach(content)
    else:
        print("Please check the mail_type before sending mail")
        return

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.sendmail(sender_mail, recipient_list, msg.as_string())
        server.close()
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
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('data/master_key.json', scope)
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1M-IQ-iYji-dbJSkrPehh3CMLiLGlzWZBzzGqVWzJPog/edit?usp=sharing")
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
    tz = tz_from.numberToTimeZone() #tz = "US/Pacific"
    mask = (df['DT Start'] < now_utc) & (df['DT End'] >= now_utc) & (df['time zone'] == tz)
    result = df.loc[mask]
    match = result.head(1)
    match = int(match['Number'])
    
    # log to console if necessary (default=False)
    if verbose:
        print(f"dataframe shape {dataframe.shape}") # all results shape
        print(f"result shape: {result.shape}") # candidate matches shape
    
    return match

# backup db
def dump_db(DB_HOST, DB_PORT, DB_USER, DB_NAME, **kwargs):
    """Function to backup database using pg_dump"""
    dump_success = 1
    command = f'pg_dump --host={DB_HOST} ' \
            f'--port={DB_PORT} ' \
            f'--username={DB_USER} ' \
            f'--dbname={DB_NAME} ' \
            f'--no-owner ' \
            f'--no-password ' \
            f'--format=c ' \
            f'--file=pgbackup`date +%F-%H%M`.dump '
    try:
        proc = subprocess.Popen(command, shell=True, env={
                    'PGPASSWORD':  os.environ['postgreSQLpass'] # DB_PASSWORD
                    })
        proc.wait()

    except Exception as e:
        dump_success = 0
        print(f"Exception happened during dump {e}")

    if dump_success:
        print('db dump successfull')

class GoogleSheetHelper:
    """Helper claas to pull data from googlesheets"""
    def __init__(self, cred_json, spreadsheetName, sheetName):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.cred_json = cred_json
        self.spreadsheetName = spreadsheetName
        self.sheetName = sheetName
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.cred_json, self.scope)
        self.client = gspread.authorize(self.creds)

    def getDataframe(self):
        """Returns all rows data from sheet as dataframe"""
        spreadsheet = self.client.open(self.spreadsheetName)
        sheet = spreadsheet.worksheet(self.sheetName)
        rows = sheet.get_all_records()
        return pd.DataFrame(rows)

    def getDict(self):
        """Returns all rows data from sheet as dictionary--one dict per row"""        
        spreadsheet = self.client.open(self.spreadsheetName)
        sheet = spreadsheet.worksheet(self.sheetName)
        return sheet.get_all_records()

    def viewAllClientSheets(self):
        """Returns sheets this gspread (self.client) authorized to view/edit"""
        available_sheets = self.client.openall()
        return [sheet.title for sheet in available_sheets]
