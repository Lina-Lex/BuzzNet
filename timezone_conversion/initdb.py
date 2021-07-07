from peewee import *
from models import db, Patient
from utils import *

# initialize db
db = SqliteDatabase('respondNoTwilio.db')
db.connect() # important

# query all users and print them
print("\n[INFO] Querying and printing all users...")
query_all()


#now = datetime.datetime.utcnow()
query = (Patient
         .select(Patient.username, Patient.phone, Patient.timezone, Patient.timestamp, Patient.utc_start, Patient.utc_end)
         .where(
            Patient.timezone == "US/Pacific", Patient.utc_start > datetime.datetime.utcnow()) 
            )

print("\n[INFO] Querying only US/Pacific users...")
for (i, row) in enumerate(query):
   print(i, f"name: {row.username} phone: {row.phone} timezone: {row.timezone} timestamp: {row.timestamp}    utc_start: {row.utc_start} utc_end: {row.utc_end}\n")

db.close()
