# Remove any existing database file first
import os
from utils import *

# remove db if exits, because will make duplicates if not each time code is run
if os.path.exists('simple.db'):
    print("\nDatabase already exists...removing...\n")
    os.remove('simple.db')

# Create database and tables
from models import db, Patient
db.connect()
db.create_tables([Patient])

# fake users
numbers = ["16692419870", "16617480240", "14436533745"]
available = [["3 pm", "7 pm"], ["11 am", "3 pm"], ["11 am", "3 pm"]]
names = [fake.name() for i in range(len(numbers))]
zones = [convertNumberToTimeZone(i) for i in numbers]

# format availability and convert local start, stop times to utc stop start times (need each start, stop times local zone to be able to localize it then conver to utc)
available = availabilityToUTC(available)
times = []
for idx, i in enumerate(available):
    row = convertLocalStartToUtcStart(zones[idx], available[idx][0]), convertLocalStartToUtcStart(zones[idx], available[idx][1])

    print(row[0], "-", row[1])
    times.append(row)

# add to db all rows of users
rows = zip(names, numbers)
for idx, row in enumerate(rows):
    p = Patient(
            username=row[0], 
            phone=row[1], 
            timezone=convertNumberToTimeZone(row[1]), 
            utc_start=times[idx][0],
            utc_end=times[idx][1]
            #duration
            # timestamp (utc) default
            )
    p.save() # each row now stored in database

# close conn
db.close()


