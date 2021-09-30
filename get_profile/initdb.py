# imports
import os
import datetime
from datetime import timedelta

# remove db if exits, because will make duplicates if not each time code is run
if os.path.exists('profileinfo.db'):
    print("\nDatabase already exists...removing...\n")
    os.remove('profileinfo.db')

# Create database and tables
from models import db, Patient
db.connect()
db.create_tables([Patient]) # Person for testing purposes

users = [
    {"username": "Alice", "phone": "16692419870",
    "calltime": timedelta(0,0,0,0,30,5), "timezone" : "US/Pacific", "type" : "Patient"},

    {"username": "Elizabeth", "phone": "16617480240", 
    "calltime": timedelta(0,0,0,0,30,5), "timezone" : "US/Pacific", "type" : "Patient"},

    {"username": "Tim", "phone": "14436533745",  
    "calltime": timedelta(0,0,0,0,30,5), "timezone" : "US/Pacific", "type" : "Patient"}
]

for d in users:
    p = Patient(
            username=d["username"], 
            phone=d["phone"],
            calltime=d["calltime"],# 5 hours
            timezone=d["timezone"],
            type=d["type"]
            )
    p.save() # each row now stored in database

# close conn
db.close()
