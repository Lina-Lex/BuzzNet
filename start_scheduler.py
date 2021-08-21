import sys
import subprocess

from multiprocessing import Process
from threading import Thread, Event,Lock

WORKER_CMD = ['celery', '-A', 'taskscheduler.celery_app', 'worker', '-c', '5', '--loglevel=info']
BEAT_CMD = ['celery', '-A', 'taskscheduler.celery_app', 'beat', '--loglevel=info']
POOL = {}
lock = Lock()
event = Event()

def start_worker():
    global POOL
    worker_process = subprocess.Popen(args=WORKER_CMD, stdout=subprocess.PIPE)
    lock.acquire()
    with open('worker_pid.PID',"w") as fd:
        fd.write(str(worker_process.pid))
    POOL["worker_process"]=worker_process
    print(POOL)
    lock.release()
    
    

def start_beat():
    global POOL
    beat_process = subprocess.Popen(args=BEAT_CMD, stdout=subprocess.PIPE)
    lock.acquire()
    with open('beat_pid.PID',"w") as fd:
        fd.write(str(beat_process.pid))
    POOL["beat_process"]=beat_process
    print(POOL)
    lock.release()


def shutdown():
    print("Shuting down the processes")
    print(POOL)
    b = POOL.get("beat_process")
    w = POOL.get("worker_process")
    b.terminate()
    print(f"Beat terminated")
    w.terminate()
    print("workers terminated")


if __name__ == "__main__":

    try:
        t_worker = Thread(target=start_worker,daemon=True)
        t_worker.start()
        t_beat = Thread(target=start_beat,daemon=True)
        t_beat.start()
        event.wait()
    except (Exception,KeyboardInterrupt) as e:
        print("Exiting ", e)
        shutdown()

        
