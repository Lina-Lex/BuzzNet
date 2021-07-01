# Remove any existing database file first
import os
from utils import *

# remove db if exits, because will make duplicates if not each time code is run
if os.path.exists('simple.db'):
    os.remove('simple.db')

# Create database and tables
from models import db, Patient

db.connect()
db.create_tables([Patient])

# fake users
numbers = ["16692419870", "16617480240", "14436533745"]
#available = ["3 pm to 7 pm", "11 am to 3 pm", "11 am to 3 pm"] # utc start, utc end
available = [["3 pm", "7 pm"], ["11 am", "3 pm"], ["11 am", "3 pm"]]

zones = [convertNumberToTimeZone(i) for i in numbers]
names = [fake.name() for i in range(len(numbers))]
utc = [local_to_utc(convertNumberToTimeZone(i)) for i in numbers] # not used in zip below
utc_start, utc_end = availabilityToUTC(available)


# add to db all rows of users
rows = zip(names, numbers, available, zones)
for row in rows:
    p = Patient(
            username=row[0], 
            phone=row[1], 
            timezone=convertNumberToTimeZone(row[1]), 
            availability=row[2],
            utc_start=utc_start,
            utc_end=utc_end
            # timestamp (utc) default
            )
    p.save() # each row now stored in database

# close conn
db.close()


