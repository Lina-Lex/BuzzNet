from datetime import timedelta,datetime
from .tasks import celery_app
from .celeryconfig import config
from peewee import *

### update config ###
celery_app.conf.update(config)



##### define heart beet tasks ########

@celery_app.create_beat(name= 'schedule-tasks-from-DB')
def get_data_and_schedule_call():
    db = PostgresqlDatabase('patient', user='postgres', password='test123',host='127.0.0.1',port=5432)
    cur = db.execute_sql('select phone,username,timezone from patient')
    val = cur.fetchall()
    plugged_task_list =celery_app.get_plugged_tasklist()

    #####################
    time = datetime.utcnow() + timedelta(seconds=7)
    # THE above line should be replaced with the timezone eta column in DB for each user

    for i in val:
        for t_name ,task in plugged_task_list.items():
            task.apply_async(args=(i,),eta=time)



@celery_app.create_beat(name='get-profile-details-weekly')
def get_profile_details():
    
    ''' Not using any task function because calling the function 
        directly inside the beat which is scheduled weekly'''
    
    from flaskapp.core.ivr_core import profile_detail
    profile_detail()

@celery_app.create_beat(name='gspread_to_postgres')
def gspread_to_postgess():
    ''' Copies google_sheets to postgres every 2 days '''

    from gspread_to_postgres import execute
    execute()
@celery_app.create_beat(name= 'get-profile-details-daily')
def get_profile_details_daily():
    plugged_task_list =celery_app.get_plugged_tasklist()
    time_min = datetime.utcnow().replace(hour=19, minute=00, second=00, microsecond=00000)

    for t_name ,task in plugged_task_list.items():
        task.apply_async(args=(1,),eta=time_min)