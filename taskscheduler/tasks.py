from flaskapp.core.ivr_core import insert_or_update_feedback, out_bound_call
from .tools import CeleryTask

#########################################
# celelry application : dont change or delete

celery_app = CeleryTask('Task-Scheduler')


#########################################


##### define proxy tasks for you tasks below #######


@celery_app.add_task(plug_to='schedule-tasks-from-DB')
# @celery_app.block_exc
def proxy_task1(*arg, **kw):
    from flaskapp.core.ivr_core import profile_detail
    profile_detail()


@celery_app.task(name="make_call_to_get_feedback")
def make_call_to_get_feedback(phone):
    out_bound_call(phone)


@celery_app.task(name="insert_into_feedback_table")
def insert_into_feedback(phone):
    insert_or_update_feedback(phone)
