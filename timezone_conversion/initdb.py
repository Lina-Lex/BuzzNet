# imports
import os
from utils import *
from timezoneHelperClass import TimeZoneHelper

# remove db if exits, because will make duplicates if not each time code is run
if os.path.exists('respondNoTwilio.db'):
    print("\nDatabase already exists...removing...\n")
    os.remove('respondNoTwilio.db')

# Create database and tables
from models import db, Patient, Person
db.connect()
db.create_tables([Patient, Person]) # Person for testing purposes

# # Add sample data
# datetime.datetime(year, month, day, hour, minute)
utc_start = datetime.datetime(2021, 7, 6, 6, 0, 0)
utc_end = datetime.datetime(2021, 7, 6, 6, 0, 0)

users = [
    {"username": "Alice", "phone": "16692419870", "utc_start" : utc_start, "utc_end" : utc_end},
    {"username": "Elizabeth", "phone": "16617480240", "utc_start" : utc_start, "utc_end" : utc_end},
    {"username": "Tim", "phone": "14436533745",  "utc_start" : utc_start, "utc_end" : utc_end},
]

tz = TimeZoneHelper("16692419870")
tz.numberToTimeZone() 
print(tz.utcToLocal())


#print(users["utc_start"])
for d in users:
    tz = TimeZoneHelper(d["phone"])
    p = Patient(
            username=d["username"], 
            phone=d["phone"],
            utc_start=d["utc_start"],
            utc_end=d["utc_end"],
            timezone=tz.numberToTimeZone()
            )
    p.save() # each row now stored in database

    # close conn
db.close()

# query all users and print them
print("\n[INFO] Querying and printing all users Pacific Time...")
query_all()

query = (Patient
         .select(Patient.username, Patient.phone, Patient.utc_start, Patient.utc_end)
         .where(
            (Patient.timezone == "US/Pacific"),
            Patient.utc_start > datetime.datetime.utcnow()
            )
         )

print("\n[INFO] Querying only US/Pacific users...")
for (i, row) in enumerate(query):
   print(i, f"name: {row.username} phone: {row.phone} utc_start: {row.utc_start} utc_end: {row.utc_end}\n")

db.close()
