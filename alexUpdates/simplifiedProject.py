from peewee import *
import pandas as pd
import numpy as np
import phonenumbers
from phonenumbers import geocoder
from phonenumbers.timezone import time_zones_for_number
from faker import Faker
import datetime
import pytz
import os

# initialize faker object for "fake" users and load mappings (State to Time Zone)
fake = Faker()
tzs_df = pd.read_csv("tzmapping.csv")
tzs_df.index = tzs_df['State']

# query all users and print them
def query_all():
    rows = Patient.select()
    for (i, row) in enumerate(rows):
       print(i, f"name: {row.username} phone: {row.phone} timezone: {row.timezone} availability: {row.availability} timestamp: {row.timestamp} utc: {row.utc}")
    db.close()

# converts a phone number to a timezone
def convertToTimeZone(number):  
    fmtNum = phonenumbers.parse("+" + str(number))
    state = geocoder.description_for_number(fmtNum, 'en')
    time_zone = tzs_df.loc[state]['Zone']
    fmtTimeZone = "US/" + time_zone.split(" ")[0]
    return fmtTimeZone

# zone = "US/Pacific"
def convertToUTC(zone):  
    dt = datetime.datetime.now()
    localized_dt = pytz.timezone(zone)
    dt = localized_dt.localize(dt)

    target_tz = pytz.timezone("UTC")
    normalizedUTC = target_tz.normalize(dt)
    return normalizedUTC

# remove db if exits, because will make duplicates if not each time code is run
if os.path.exists('simple.db'):
    os.remove('simple.db')

# initialize db
db = SqliteDatabase('simple.db')

# Base model for work with Database through ORM
class BaseModel(Model):
    class Meta:
        database = db  # connection with database

class Patient(BaseModel):
    id = AutoField(column_name='ID')
    phone = TextField(column_name='Phone', null=True)
    username = TextField(column_name='Username', null=True)
    gender = TextField(column_name='Gender', null=True)
    timezone = TextField(column_name='Timezone', null=True)
    availability = TextField(column_name='Availability', null=True) # NEW FIELD
    utc = TimeField(column_name='UTC', null=True) # NEW FIELD
    timestamp = DateTimeField(column_name='Timestamp', default=datetime.datetime.now, null=False) # NEW FIELD
    callstart = TimeField(column_name='CallStart', null=True)
    callend = TimeField(column_name='CallEnd', null=True)
    type = TextField(column_name='Type', null=True)
    created = DateTimeField(column_name='Created', null=True)
    updated = DateTimeField(column_name='Updated', null=True)
    class Meta:
        table_name = 'Patient'

# connect + create Patient table in "simple.db" database
db.connect()
db.create_tables([Patient])

# fake users
numbers = ["16692419870", "16617480240", "14436533745"]
available = ["3 pm to 7 pm", "11 am to 3 pm", "11 am to 3 pm"]
time_zones = [convertToTimeZone(i) for i in numbers]
names = [fake.name() for i in range(len(numbers))]
utc = [convertToUTC(convertToTimeZone(i)) for i in numbers]

# add to db all rows of users
rows = zip(names, numbers, available, utc)
for row in rows:
    p = Patient(
            username=row[0], 
            phone=row[1], 
            timezone=convertToTimeZone(row[1]), 
            availability=row[2],
            utc=convertToUTC(convertToTimeZone(row[1]))
            #utc_availability=??
            )
    p.save() # each row now stored in database

# close conn
db.close()

# query all users and print them
print("\nQuerying and printing all users...")
query_all()

# Alex example --> pat = Patient.get(Patient.phone == tel)
#print(pat.id, pat.phone)
query = (Patient
         .select(Patient.username, Patient.phone, Patient.timezone, Patient.availability, Patient.timestamp, Patient.utc)
         .where(
             (Patient.timezone == "US/Pacific")
             # Patient.available == True
         ))

print("\nQuerying only US/Pacific users...")
for (i, row) in enumerate(query):
   print(i, f"name: {row.username} phone: {row.phone} timezone: {row.timezone} availability: {row.availability} timestamp: {row.timestamp} utc: {row.utc}")
db.close()
