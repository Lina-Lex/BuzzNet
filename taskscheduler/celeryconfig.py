from datetime import timedelta

# Default timezone is UTC for celery 

config = {
    "broker_url":"pyamqp://guest@localhost//",
    "task_serializer":"json",
    "result_serializer":'json',
    "accept_content":['json'],
    # "timezone":'',
    "enable_utc":True,
    "beat_schedule":{
    "call-DB-and-schedule-task": {
        'task': 'schedule-tasks-from-DB',
        'schedule': timedelta(seconds=5)
    },
    'weekly-profile-details':{
        'task':'get-profile-details-weekly',
        'schedule':timedelta(days=7)
    }
}
}