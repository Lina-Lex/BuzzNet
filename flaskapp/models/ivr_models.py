import datetime
from peewee import (AutoField, TextField, DateTimeField,
                    Model, ForeignKeyField)

from flaskapp.models.bases import BaseModel, DatesMixin
from playhouse.postgres_ext import BinaryJSONField
from flaskapp.models.storages import postgress_conn


class User(DatesMixin, BaseModel):
    """ General user model """

    id        = AutoField()               # noqa: E221
    phone     = TextField(null=True)      # noqa: E221
    username  = TextField(null=True)      # noqa: E221
    gender    = TextField(null=True)      # noqa: E221
    timezone  = TextField(null=True)      # noqa: E221
    type      = TextField(null=True)      # noqa: E221

    class Meta:
        table_name = 'users'


class Call(DatesMixin, BaseModel):
    id         = AutoField()              # noqa: E221
    call_start = DateTimeField()          # noqa: E221
    call_end   = DateTimeField()          # noqa: E221
    user       = ForeignKeyField(         # noqa: E221
        User,
        backref='calls',
        on_delete='CASCADE'
    )

    class Meta:
        table_name = 'calls'


class HealthMetric(DatesMixin, BaseModel):
    id         = AutoField()               # noqa: E221
    user       = ForeignKeyField(          # noqa: E221
        User,
        backref='health_metrics',
        on_delete='CASCADE'
    )

    data       = BinaryJSONField()         # noqa: E221

    class Meta:
        table_name = 'health_metrics'


# Reminder
class Reminder(BaseModel):
    id = AutoField(column_name='ID')
    text = TextField(column_name='text', null=True)

    class Meta:
        table_name = 'reminders'


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
        table_name = 'smartreminders'


# TODO: Review and restructurization needed
def db_create_tables(conn):

    conn.drop_tables([Patient, Reminder, SmartReminder])

    conn.create_tables([Patient, Reminder, SmartReminder])
    conn.commit()

    conn.cursor().execute("INSERT INTO Patient(Phone, Username, Gender, Timezone, CallStart,CallEnd, Type, Created, Updated) VALUES ('13333333333', 'Alex', 'Male', 'Pacific Standard Time', '16:00:00', '18:00:00', 'Volunteer', now(), now())")
    conn.cursor().execute("INSERT INTO Patient (Phone, Username, Gender, Timezone, CallStart,CallEnd, Type, Created, Updated) VALUES ('12222222222', 'Lina', 'Male', 'Pacific Standard Time', '16:00:00', '18:00:00', 'Volunteer', now(), now())")
    conn.cursor().execute("INSERT INTO Reminder (Text) VALUES ('Get at least 150 minutes per week of moderate-intensity aerobic activity or 75 minutes per week of vigorous aerobic activity, or a combination of both, preferably spread throughout the week.')")
    conn.cursor().execute("INSERT INTO Reminder (Text) VALUES ( 'Add moderate- to high-intensity muscle-strengthening activity (such as resistance or weights) on at least 2 days per week.')")
    conn.cursor().execute("INSERT INTO Reminder (Text) VALUES ( 'Spend less time sitting. Even light-intensity activity can offset some of the risks of being sedentary.')")
    conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('1', '1', now())")
    conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('1', '2', now())")
    conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('1', '3', now())")
    conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('2', '1', now())")
    conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('2', '2', now())")
    conn.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('2', '3', now())")

    conn.commit()

# TODO: Review and restructurization needed
def init_db(conn):
    with conn.atomic() as transaction:  # Opens new transaction.
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
    conn.close()


#============== creating entries in DB =========================
if __name__ == "__main__":
    print ('start db connect...')
    db_proxy.connect()
    print('init db...')
    init_db(postgress_conn)