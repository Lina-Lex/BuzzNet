import datetime
import pytz
from pytz import timezone
import phonenumbers
from phonenumbers import geocoder
from faker import Faker
import pandas as pd

from models import db, Patient

# initialize faker object for "fake" users and load mappings (State to Time Zone)
fake = Faker()
tzs_df = pd.read_csv("./data/tzmapping.csv")
tzs_df.index = tzs_df['State']

# query all users and print them
def query_all():
    rows = Patient.select()
    for (i, row) in enumerate(rows):
       print(i, f"name: {row.username} phone: {row.phone} timezone: {row.timezone} timestamp: {row.timestamp} utc_start: {row.utc_start} utc_end: {row.utc_end}\n")
    db.close()

# converts a phone number to a timezone
def convertNumberToTimeZone(number):  
    fmtNum = phonenumbers.parse("+" + str(number))
    state = geocoder.description_for_number(fmtNum, 'en')
    time_zone = tzs_df.loc[state]['Zone']
    fmtTimeZone = "US/" + time_zone.split(" ")[0]
    return fmtTimeZone

# converts utc to a local time
def utc_to_localtime(tz):
    utc_time = datetime.datetime.utcnow()
    utc_to_local = pytz.utc.localize(utc_time, is_dst=None).astimezone(tz)
    return utc_to_local

# converts local time to utc
def local_to_utc(zone):  
    dt = datetime.datetime.now()
    localized_dt = pytz.timezone(zone)
    dt = localized_dt.localize(dt)

    target_tz = pytz.timezone("UTC")
    normalizedUTC = target_tz.normalize(dt)
    return normalizedUTC

def convertLocalStartToUtcStart(zone, localStart):
    today = datetime.datetime.today() #tz_info??
    dt = today.replace(hour=localStart, minute=00)

    localized_dt = pytz.timezone(zone)
    dt = localized_dt.localize(dt)

    target_tz = pytz.timezone("UTC")
    normalizedUTCStart = target_tz.normalize(dt)
    return normalizedUTCStart


def availabilityToUTC(available):
    output = []
    for i, avail in enumerate(available):
        utc_start, utc_end = avail
        utc_start = int(utc_start.split(" ")[0])
        utc_end = int(utc_end.split(" ")[0])
        row = [utc_start, utc_end]
        output.append(row)
    return output
