from datetime import timedelta,datetime
from .tasks import celery_app
from .celeryconfig import config
from peewee import *
import os
import subprocess
import datetime

### update config ###
celery_app.conf.update(config)



##### define heart beet tasks ########

@celery_app.create_beat(name= 'schedule-tasks-from-DB')
def get_data_and_schedule_call():
    db = PostgresqlDatabase('patient', user='postgres', password='test123',host='127.0.0.1',port=5432)
    cur = db.execute_sql('select phone,username,timezone from patient')
    val = cur.fetchall()
    plugged_task_list =celery_app.get_plugged_tasklist()

    time = datetime.utcnow() + timedelta(seconds=7)

    for i in val:
        for t_name ,task in plugged_task_list.items():
            task.apply_async(args=(i,),eta=time)



@celery_app.create_beat(name='get-profile-details-weekly')
def get_profile_details():
    
    ''' Not using any task function because calling the function 
        directly inside the beat which is scheduled weekly'''
    
    from main import profile_detail
    profile_detail()

    
@celery_app.create_beat(name='backup-db')
def backup_db():
    ''' Not using any task function because calling the function 
        directly inside the beat which is scheduled ???'''
    
    DB_NAME = 'goanddo'  # your db name
    DB_USER = 'postgres' # you db user
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_PASSWORD = os.environ['postgreSQLpass'] # your db password
    
    from util import dump_schema
    dump_schema(DB_HOST, DB_PORT, DB_USER, DB_NAME)
