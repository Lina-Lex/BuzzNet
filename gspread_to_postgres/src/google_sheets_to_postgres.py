import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import sqlalchemy as sa
from sqlalchemy.engine import make_url
# from sqlalchemy.types import Integer, Text, String, DateTime
import datetime

from threading import Thread 
from queue import Queue

class Worker(Thread):
    def __init__(self ,queue = None,*args,**kw):
        self.callback = kw.get('target',None)
        self.queue = queue
        super().__init__(*args,**kw)
    
    def run(self):
        while True:
            engine,main_sheet,wrksht =  self.queue.get()
            self.callback(engine,main_sheet,wrksht)
            self.queue.task_done()

class GoogleSheetHelper:
    """Helper class to pull data from googlesheets"""
    def __init__(self, cred_json, spreadsheetName):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.cred_json = cred_json
        self.spreadsheetName = spreadsheetName
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.cred_json, self.scope)
        self.client = gspread.authorize(self.creds)
        self.spreadsheet = self.client.open(self.spreadsheetName)

    def getDataframe(self,worksheet):
        """Returns all rows data from sheet as dataframe"""
        sheet = self.spreadsheet.worksheet(worksheet)
        rows = sheet.get_all_records()
        return pd.DataFrame(rows)

    def getAllWorksheet(self):
        # spreadsheet = self.client.open(self.spreadsheetName)
        return [s.title for s in self.spreadsheet.worksheets()] 

    def getAllSpreadsheets(self):
        """Returns sheets this gspread (self.client) authorized to view/edit"""
        available_sheets = self.client.openall()
        print(available_sheets)
        return [sheet.title for sheet in available_sheets]


def _set_url_database(url , databasename):
    """creates url with provided DB for the engine """

    url = make_url(url)
    if hasattr(sa.engine, 'URL'):
        res = sa.engine.URL.create(
            drivername=url.drivername,
            username=url.username,
            password=url.password,
            host=url.host,
            port=url.port,
            database=databasename,
            query=url.query
        )
    else:  # SQLAlchemy <1.4
        url.database = databasename
        res = url

    return res


def create_db_if_not_exists(url:str,dbname:str):
    """Check and Creates DB as per the Db name if it doesnot exists """

    query  =  f"SELECT 1 FROM pg_database WHERE datname='{dbname}'"
    en = sa.create_engine(url,isolation_level="AUTOCOMMIT", echo=False)
    with en.connect() as con:
        r = con.scalar(query)
        if not r:
            sql = f'CREATE DATABASE "{dbname}"'
            con.execute(sql)


def create_table(engine,main_sheet,wrksht):
    """ Function thats actualy takes the Database and creates a entry inside the postgresSQL server"""

    df = main_sheet.getDataframe(wrksht)
    table_name = wrksht
    current_utc = datetime.datetime.utcnow()
    df["CreatedUTC"] = current_utc
    df.to_sql(
        table_name,
        engine,
        if_exists='replace',
        index=False,
        chunksize=500,
    )
    return True

    
def execute(max_worker = 5):
    """ The main function that create the migration and performes it """
    if max_worker > 15:
        raise RuntimeError("cannot creat workers above 15")

    from .settings import Spreadsheet_config as sp_config
    from .settings import PostgresSQL_config as psql_config

    if psql_config.__dict__.get('database'):
        database =  psql_config.database
    else:
        database =  sp_config.spreadsheet_name
    
    DBDRIVER = psql_config.__dict__.get("DRIVER","postgresql")
    
    uri = f"{DBDRIVER}://{psql_config.username}:{psql_config.password}@{psql_config.host}:{psql_config.port}"
    create_db_if_not_exists(uri,database)

    url_with_db = _set_url_database(uri,database)
    
    engine = sa.create_engine(url_with_db, echo=False)

    main_sheet = GoogleSheetHelper(sp_config.credential_path, sp_config.spreadsheet_name)

    if sp_config.backup_all_worksheets:
        wrksheet_list = main_sheet.getAllWorksheet()
    else:
        wrksheet_list =  sp_config.worksheet_to_consider

    qu = Queue()  
    threadlist = []
    for _ in range(max_worker):
        t = Worker(queue=qu,target=create_table,daemon=True)
        t.start()
        # threadlist.append(t)

    for wrksht in wrksheet_list:
        # create_table(engine,main_sheet,wrksht)
        qu.put((engine,main_sheet,wrksht))
    qu.join()

        
    
        