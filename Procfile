web: gunicorn main:app --log-file=-
worker: celery -A taskscheduler.celery_app worker -c 5 --loglevel=info
beat: celery -A taskscheduler.celery_app beat --loglevel=info