from datetime import timedelta, datetime
from .tasks import celery_app
from .celeryconfig import config
from peewee import *

### update config ###
celery_app.conf.update(config)


##### define heart beet tasks ########

@celery_app.create_beat(name='schedule-tasks-from-DB')
def get_data_and_schedule_call():
    db = PostgresqlDatabase('patient', user='postgres', password='test123', host='127.0.0.1', port=5432)
    cur = db.execute_sql('select phone,username,timezone from patient')
    val = cur.fetchall()
    plugged_task_list = celery_app.get_plugged_tasklist()

    time = datetime.utcnow() + timedelta(seconds=7)

    for i in val:
        for t_name, task in plugged_task_list.items():
            task.apply_async(args=(i,), eta=time)


@celery_app.create_beat(name='Demo')
def dis():
    print('Demo')
    celery_app.get_plugged_tasklist()
