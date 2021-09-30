from peewee import *
from models import db, Patient
import json
from playhouse.shortcuts import model_to_dict

def print_models(models):
    print(json.dumps(list(models.dicts()), indent=4, sort_keys=True, default=str))

# initialize db
db = SqliteDatabase('profileinfo.db')
db.connect()

# query all users and print them
print("\n[INFO] Querying and printing all users...")
#query_all()

#now = datetime.datetime.utcnow()
query = (Patient
         .select(Patient.username, Patient.phone, Patient.calltime, Patient.timezone, Patient.type))
         # .where(
         #    Patient.timezone == "US/Pacific" # must comma here if add more filter criteria
         #    ))

print("\n[INFO] Querying only US/Pacific users...")
for (i, row) in enumerate(query):
   print(i, f"name: {row.username} phone: {row.phone} calltime: {row.calltime} type: {row.type}\n")

print_models(query)
db.close()

