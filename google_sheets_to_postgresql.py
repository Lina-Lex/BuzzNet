import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, String, DateTime
import datetime

# import util for GoogleSheetHelper class
from util import *

# setup credentials
cred_json = os.environ['json_path']
df1 = GoogleSheetHelper(cred_json, "Users", "existing")
df2 = GoogleSheetHelper(cred_json, "Users", "calls")
df3 = GoogleSheetHelper(cred_json, "Users", "time")
#print(df1.getDataframe().head()) # prints first 5 rows

# all worksheets avaialble for this google key
all_sheets = df1.viewAllClientSheets()
#print(all_sheets) # print list of all available sheets for that key

# sanity check / will use for unit test
print("[x] printing columns...")
print(df1.getDataframe().columns)
print(df2.getDataframe().columns)
print(df3.getDataframe().columns)

###############################################################################
# Now that we have data from googlesheetsAPI, insert to goanddo PostgresSQL
###############################################################################
host = "localhost"
port = 5432
username = "postgres"
password = os.environ['postgreSQLpass']

database = "goanddo" 

db_uri = f"postgresql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(db_uri, echo=True)

# existing sheet inside Users worksheet
existing_df = df1.getDataframe()
table_name = 'User_existing'
current_utc = datetime.datetime.utcnow()
existing_df["CreatedUTC"] = current_utc
existing_df.to_sql(
    table_name,
    engine,
    if_exists='replace',
    index=False,
    chunksize=500,
)

table_df = pd.read_sql_table(
    table_name,
    con=engine
)

print(table_df.head())

# calls sheet inside Users worksheet
calls_df = df2.getDataframe() 
table_name = 'User_calls'
current_utc = datetime.datetime.utcnow()
calls_df["CreatedUTC"] = current_utc
calls_df.to_sql(
    table_name,
    engine,
    if_exists='replace',
    index=False,
    chunksize=500,
)

table_df = pd.read_sql_table(
    table_name,
    con=engine
)

print(table_df.head())

# time sheet inside Users worksheet
time_df = df3.getDataframe() 
table_name = 'User_time' # + utc for unique backup?
current_utc = datetime.datetime.utcnow()
time_df["CreatedUTC"] = current_utc
time_df.to_sql(
    table_name,
    engine,
    if_exists='replace',
    index=False,
    chunksize=500,
)

table_df = pd.read_sql_table(
    table_name,
    con=engine
)

print(table_df.head())

"""
Asana task description:
Why: there is a limit on the scalability of the architecture in the google spreadsheet. 
It is necessary to exclude all the code for working with Google spreadsheet and replace it with working with a database (PostgreSQL).
Prepare function Init which will automatically migrate data from the current table structure to a new one do not miss existing data.
As result, changes should make a backup of the data, create a new database with a new structure, and upload data from the backup.
"""

