# imports
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
names = [fake.name() for i in numbers]
zones = [convertNumberToTimeZone(i) for i in numbers]

# extract digits from each element of list of lists in availabile variable 
fmtAvailable = extractAvailabilityFromList(available)

# use fmtAvailable list of lists from above to get availability times converted to utc as list of lists
times = formattedAvailabilityListToUTC(zones, fmtAvailable)

# add to db all rows of users
rows = zip(names, numbers, times)
for idx, row in enumerate(rows):
    p = Patient(
            username=row[0], 
            phone=row[1], 
            timezone=convertNumberToTimeZone(row[1]), 
            utc_start=row[2][0],
            utc_end=row[2][1],
            )
    p.save() # each row now stored in database

# close conn
db.close()


