from datetime import timedelta

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
    }
    # 'every-10-sec':{
    #     'task':'display',
    #     'schedule':timedelta(seconds=10)
    # }
}

}