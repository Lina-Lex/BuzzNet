import datetime
from peewee import (AutoField, TextField, DateTimeField, TimeField, Proxy,
                    Model, ForeignKeyField)
from playhouse.postgres_ext import BinaryJSONField
from flaskapp.models.storages import postgress_conn

db_proxy = Proxy()


# Base model for work with Database through ORM
class BaseModel(Model):
    class Meta:
        database = db_proxy  # connection with database


# NOTE:  Dynamic db-switching is absolutely unnecessary
# However, this construction will be useful when testing
db_proxy.initialize(postgress_conn)


# Patient model
class User(BaseModel):
    id        = AutoField()
    phone     = TextField(null=True)
    username  = TextField(null=True)
    gender    = TextField(null=True)
    timezone  = TextField(null=True)
    type      = TextField(null=True)
    created   = DateTimeField(default=datetime.datetime.now, null=True)
    updated   = DateTimeField(null=True)

    class Meta:
        table_name = 'users'


class Call(BaseModel):
    id         = AutoField()
    call_start = DateTimeField()
    call_end   = DateTimeField()
    user       = ForeignKeyField(User, backref='calls', on_delete='CASCADE')

    class Meta:
        table_name = 'calls'


class HealthMetric(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='health_metrics', on_delete='CASCADE')
    data = BinaryJSONField()

    class Meta:
        table_name = 'health_metrics'


# Reminder
class Reminder(BaseModel):
    id = AutoField(column_name='ID')
    text = TextField(column_name='text', null=True)

    class Meta:
        table_name = 'reminder'


# Smart Reminder
class SmartReminder(BaseModel):
    id = AutoField(column_name='ID')
    patient_id = IntegerField(column_name='patientid')
    reminder_id = IntegerField(column_name='reminderid')

    easiness = FloatField(column_name='easiness', null=True)
    interval = IntegerField(column_name='interval', null=True)
    repetitions = IntegerField(column_name='repetitions', null=True)

    last_time = DateTimeField(column_name='lasttime', null=True)
    next_time = DateTimeField(column_name='nexttime', null=True)

    class Meta:
        table_name = 'smartreminder'


def db_create_tables():
    postgres_conn.drop_tables([Patient, Reminder, SmartReminder])
    # postgres_conn.cursor().execute("drop table patient")
    # postgres_conn.cursor().execute("drop table reminder")
    # postgres_conn.cursor().execute("drop table smartreminder")

    postgres_conn.create_tables([Patient, Reminder, SmartReminder])
    postgres_conn.commit()

    postgres_conn.cursor().execute("INSERT INTO Patient(Phone, Username, Gender, Timezone, CallStart,CallEnd, Type, Created, Updated) VALUES ('13333333333', 'Alex', 'Male', 'Pacific Standard Time', '16:00:00', '18:00:00', 'Volunteer', now(), now())")
    postgres_conn.cursor().execute("INSERT INTO Patient (Phone, Username, Gender, Timezone, CallStart,CallEnd, Type, Created, Updated) VALUES ('12222222222', 'Lina', 'Male', 'Pacific Standard Time', '16:00:00', '18:00:00', 'Volunteer', now(), now())")
    postgres_conn.cursor().execute("INSERT INTO Reminder (Text) VALUES ('Get at least 150 minutes per week of moderate-intensity aerobic activity or 75 minutes per week of vigorous aerobic activity, or a combination of both, preferably spread throughout the week.')")
    postgres_conn.cursor().execute("INSERT INTO Reminder (Text) VALUES ( 'Add moderate- to high-intensity muscle-strengthening activity (such as resistance or weights) on at least 2 days per week.')")
    postgres_conn.cursor().execute("INSERT INTO Reminder (Text) VALUES ( 'Spend less time sitting. Even light-intensity activity can offset some of the risks of being sedentary.')")
    postgres_conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('1', '1', now())")
    postgres_conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('1', '2', now())")
    postgres_conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('1', '3', now())")
    postgres_conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('2', '1', now())")
    postgres_conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('2', '2', now())")
    postgres_conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('2', '3', now())")

    postgres_conn.commit()


def init_db():
    with postgres_conn.atomic() as transaction:  # Opens new transaction.
        try:
            db_create_tables()
            print ("tables in database created...")
        except:
            # Because this block of code is wrapped with "atomic", a
            # new transaction will begin automatically after the call
            # to rollback().
            transaction.rollback()
            print ("rollback ...")
            error_saving = True
            raise

        #create_report(error_saving=error_saving)
        # Note: no need to call commit. Since this marks the end of the
        # wrapped block of code, the `atomic` context manager will
        # automatically call commit for us.
    postgres_conn.close()


#============== creating entries in DB =========================
if __name__ == "__main__":
    print ('start db connect...')
    db_proxy.connect()
    #db_proxy.create_tables([Patient, Reminder, SmartReminder], safe=True)
    print('init db...')
    init_db()