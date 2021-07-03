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
    timestamp = DateTimeField(column_name='Timestamp', default=datetime.datetime.utcnow, null=False) # NEW FIELD
    utc_start = TimeField(column_name='UTC_Start', null=True) # NEW FIELD
    utc_end = TimeField(column_name='UTC_End', null=True) # NEW FIELD
    duration = TimeField(column_name='Duration', null=True) # NEW FIELD
    callstart = TimeField(column_name='CallStart', null=True)
    callend = TimeField(column_name='CallEnd', null=True)
    type = TextField(column_name='Type', null=True)
    created = DateTimeField(column_name='Created', null=True)
    updated = DateTimeField(column_name='Updated', null=True)
    class Meta:
        table_name = 'Patient'

# functionalize
"""def findMatch(number, db_object):
    timeZoneFromNumber = convertToTimeZone(number)
    query = (Patient
            .select(Patient.username, Patient.phone, Patient.timezone, Patient.timestamp, Patient.utc_start, Patient.utc_end)
            .where(
                (Patient.timezone == "US/Pacific"),
                # (Patient.timestamp.between(Patient.utc_start, Patient.utc_end))
                )
            )

    print(f"\n[INFO] Querying only {timeZoneFromNumber} users...")
    for (i, row) in enumerate(query):
        print(i, f"name: {row.username} phone: {row.phone} timezone: {row.timezone} availability: {row.availability} timestamp: {row.timestamp}\n")
    db.close()

number = ["16617480240"]
findMatch(number[0], db)
"""
