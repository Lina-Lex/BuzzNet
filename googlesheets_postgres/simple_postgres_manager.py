from subprocess import PIPE,Popen
import shlex
import gzip

import os
import subprocess
import datetime

DB_NAME = 'goanddo'  # your db name
DB_USER = 'postgres' # you db user
DB_HOST = "localhost"
DB_PORT = 5432
DB_PASSWORD = os.environ['postgreSQLpass'] # your db password

def dump_schema(DB_HOST, DB_PORT, DB_USER, DB_NAME, **kwargs):
    dump_success = 1
    command = f'pg_dump --host={DB_HOST} ' \
            f'--port={DB_PORT} ' \
            f'--username={DB_USER} ' \
            f'--dbname={DB_NAME} ' \
            f'--no-owner ' \
            f'--no-password ' \
            f'--format=c ' \
            f'--file=pgbackup`date +%F-%H%M`.dump '
    try:
        proc = subprocess.Popen(command, shell=True, env={
                    'PGPASSWORD': DB_PASSWORD
                    })
        proc.wait()

    except Exception as e:
        dump_success = 0
        print('Exception happened during dump %s' %(e))


    if dump_success:
        print('db dump successfull')


# dump_schema(DB_HOST, DB_PORT, DB_USER, DB_NAME)
