import inspect
from celery import Celery
from functools import wraps 
from celery.local import PromiseProxy
from celery.app.registry import TaskRegistry


###### model class to customize celery ##############

class CeleryTask(Celery):
    def __init__(self,*args,**kw):
        self.blocked_registry = {}
        self.beat_registry =  {}
        self.translate_fun_to_name= {}
        super().__init__(*args,**kw)

    def add_logs(self,fun)-> 'Decorator fun':
        print(fun)
        @wraps(fun)
        def inner(*a,**kw):
            va = fun(*a,**kw)
        return inner
    
    def block_exc(self,fun)-> 'Decorator fun':
        if isinstance(fun,PromiseProxy):
            msg = '[X] cannot block a registered task,use decorator before registering'
            raise RuntimeError(msg)

        self.blocked_registry[fun.__name__] = fun
        def inner(*a,**kw):
            return None
        return fun
    
    def add_task(self,plug_to=None)-> 'Decorator fun':
        if not isinstance (plug_to,str) and not plug_to == None:
            msg = f"[X] {plug_to} should be string or arg plug_to is required\n[params]:@add_task(plug_to=None)or str value"
            raise  AttributeError(msg)
        beat_name = plug_to
        def add_task_proxy(fun):
            if fun.__name__ in self.blocked_registry:
                return
            if not fun.__name__.startswith('proxy_'):
                msg = '[X] use the prefix "proxy_" before the function definition ,or use the "@task" decorator'
                raise RuntimeError(msg)
            @self.task
            @wraps(fun)
            def task(*a,**kw):
                fun(*a,**kw)
                return
            if beat_name:
                self.beat_registry.setdefault(beat_name,dict())[task.__name__] = task
            return task
        return add_task_proxy


    def create_beat(self,name=None)-> 'Decorator fun':
        if not isinstance (name,str):
            msg = f"[X] {name} should be string or arg name is required\n[params]:@create_beat(name='name-defined-in-config')"
            raise  AttributeError(msg)
        def decorator(fun):
            if fun.__name__ in self.translate_fun_to_name:
                msg = f"function {fun.__name__} already mapped to {self.translate_fun_to_name[fun.__name__]} "
                raise KeyError(msg)
            self.translate_fun_to_name[fun.__name__] = name
            @self.task(name=name)
            @wraps(fun)
            def task(*a,**kw):
                return fun(*a,**kw)
            return task
        return decorator

    def get_plugged_tasklist(self) -> dict:
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        calfun =  calframe[1][3]
        mapped_name=self.translate_fun_to_name.get(calfun)
        if mapped_name:
            task_map = self.beat_registry.get(mapped_name)
            return task_map
        return







