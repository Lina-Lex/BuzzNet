from peewee import *
import datetime
import pytz
from pytz import timezone
import phonenumbers
from phonenumbers import geocoder
from faker import Faker
import pandas as pd


from models import db, Patient
from utils import *

# initialize db
db = SqliteDatabase('simple.db')
db.connect() # important

# query all users and print them
print("\n[INFO] Querying and printing all users...")
query_all()

# Alex example --> pat = Patient.get(Patient.phone == tel)
#print(pat.id, pat.phone)
query = (Patient
         .select(Patient.username, Patient.phone, Patient.timezone, 
                Patient.availability, Patient.timestamp, Patient.utc, Patient.utc_start, Patient.utc_end)
         .where(
             (Patient.timezone == "US/Pacific")
            # .where((Person.birthday < d1940) | (Person.birthday > d1960)))
            # .where(Person.birthday.between(d1940, d1960)))
            # (Patient.UTC_Start < Patient.Timestamp < Patient.UTC_End)

            )
             # Patient.available == True
         )

print("\n[INFO] Querying only US/Pacific users...")
for (i, row) in enumerate(query):
   print(i, f"name: {row.username} phone: {row.phone} timezone: {row.timezone} availability: {row.availability} timestamp: {row.timestamp}  utc_start: {row.utc_start} utc_end: {row.utc_end}\n")

db.close()
# functionalize
"""def findMatch(number, db_object):
    #query_all()
    timeZoneFromNumber = convertToTimeZone(number)
    query = (Patient
            .select(Patient.username, Patient.phone, Patient.timezone, Patient.availability, Patient.timestamp)
         .where(
             #(Patient.timezone == "US/Pacific")
            (Patient.timezone == timeZoneFromNumber)
             # (Patient.UTC_Start < Patient.Timestamp < Patient.UTC_End)
            # Patient.available == True
         ))

    print(f"\n[INFO] Querying only {timeZoneFromNumber} users...")
    for (i, row) in enumerate(query):
        print(i, f"name: {row.username} phone: {row.phone} timezone: {row.timezone} availability: {row.availability} timestamp: {row.timestamp}\n")
    db.close()

number = ["16617480240"]
findMatch(number[0], db)"""