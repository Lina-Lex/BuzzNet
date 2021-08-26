from datetime import timedelta
import os
# Default timezone is UTC for celery
'''
Don't forget define BROKER_URL as local variable:
 for local machine os.environ['BROKER_URL'] = pyamqp://guest@localhost//
 for HEROKU instance os.environ['BROKER_URL'] - get result of command line: heroku config | grep CLOUDAMQP_URL
'''
config = {
    "broker_url":os.environ['BROKER_URL'],
    "task_serializer":"json",
    "result_serializer":'json',
    "accept_content":['json'],
    # "timezone":'',
    "enable_utc":True,
    "beat_schedule":{
    'weekly-profile-details':{
        'task':'get-profile-details-weekly',
        'schedule':timedelta(days=7)
    },
    'gspread_to_postgess':{
        'task':'gspread_to_postgres',
        'schedule':timedelta(days=2)
    },
    'daily-profile-details-daily':{
        'task':'get-profile-details-daily',
        'schedule':timedelta(days=1)
                            }
}
}
'''
"call-DB-and-schedule-task": {
        'task': 'schedule-tasks-from-DB',
        'schedule': timedelta(seconds=5)
    },
'''