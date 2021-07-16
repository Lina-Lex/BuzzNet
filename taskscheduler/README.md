# Task scheduler

Used to schedule task using a messaging queue and celery

## Requirement

```
Message broker (Prefered RabbitMQ)
celelry
pewee

```
## Usage 
The application structure is implemented by inheriting and customizing celery tasks and celery beat features.
* Beat functions are defined inside the 'scheduler.py' which is the entry point for the celery commands.
* Tasks are defined inside the 'tasks.py' and each task should be plugged to a beat function (preferably)
* Tasks should act as a proxy to the real function needed to be called. instruction below 
* task functions should contain the 'proxy_' prefix.

#### Recomended to add the project folder to the PYTHONPATH for proper importing and defining of tasks

-> Example
tasks.py
```
@celelry_app.add_task(plug_to='name-of-the-beat-functions')
def proxy_mytaskName(*args,**kw):
    from module import example_funtion # or import before defining tasks
    # Do something 
    # call the real function
    example_function(*args,**kw)
```
->Example beat(should be defined inside the scheduler.py)
```
@celery_app.create_beat(name='name-of-the-beat-functions') #should be same as defined in the celeryconfig.py
def dis():
    print('this is a celelry beat that runs as per the celelryconfig')
    context_tasks=celery_app.get_plugged_tasklist() # returns a dictionary of task name and task obj
    for task_name ,task_obj in context_task.items():
        task_obj.apply_async(args('arg to task in tuple',),eta=datetime_obj)
```
**To start the workers**
```
celery -A taskscheduler.celery_app worker -c 5 --loglevel=info
```
**To start the beat**
```
celery -A taskscheduler.celery_app beat --loglevel=info
```

## API Reference

* Main app object 'celery_app'  defined in the tasks.py file .Changing it will cause unexpected Errors in the Application

**celery_app.add_task(self,plug_to=None)**<br />

&nbsp;&nbsp;&nbsp;&nbsp;A decorator to add the tasks to celery workers  
&nbsp;&nbsp;&nbsp;&nbsp;variables  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;plug_to: is mandetory to be provided even if the value is None  
&nbsp;&nbsp;&nbsp;&nbsp;Return type:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Task object  

**celery_app.create_beat(self,name=None)**  

&nbsp;&nbsp;&nbsp;&nbsp;A decorator to create a beat function  
&nbsp;&nbsp;&nbsp;&nbsp;Variable:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name : should be a str  
&nbsp;&nbsp;&nbsp;&nbsp;return type:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;beat object  


**celery_app.get_plugged_tasklist(self)**

&nbsp;&nbsp;&nbsp;&nbsp;Returns the tasks mapped to the caller beat context (or called function)

&nbsp;&nbsp;&nbsp;&nbsp;return type:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dict()
```
    {task_name:task_object}

```
**celery_app.block_exc(self,fun)**  
&nbsp;&nbsp;&nbsp;&nbsp; used as a decorator to block the tasks from getting registerd  
