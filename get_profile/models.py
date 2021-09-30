from peewee import *
import pandas as pd
import numpy as np
from faker import Faker
import datetime
import os

# initialize db
db = SqliteDatabase('profileinfo.db')

# Base model for work with Database through ORM
class BaseModel(Model):
    class Meta:
        database = db  # connection with database

class Patient(BaseModel):
    id = AutoField(column_name='ID')
    phone = TextField(column_name='Phone', null=True)
    username = TextField(column_name='Username', null=True)
    timezone = TextField(column_name='Timezone', null=True)
    calltime = TextField(column_name='Calltime', null=True)  
    type = TextField(column_name='Type', null=True)  
    class Meta:
        table_name = 'Patient'

# class Person(Model):
#     field1 = CharField()
#     field2 = CharField()

#     class Meta:
#         database = db # This model uses the "people.db" database.
