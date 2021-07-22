##############################################################################
# Now that we have data from googlesheetsAPI, insert to goanddo PostgreSQL
##############################################################################
import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, String, DateTime
import datetime

# import GoogleSheetHelper class
from util import GoogleSheetHelper

# db params
host = "localhost"
port = 5432
username = "zelda"
password = "password"
database = "godo0" 

# db uri + engine
db_uri = f"postgresql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(db_uri, echo=True)

# gsh + to postgres
cred_json = "/home/batman/Desktop/google_postgres/key/master_key.json" 
gsh = GoogleSheetHelper(cred_json, "google_postgres", "existing")
# ^^ getting only one of the sheets of the 3 available

users_df = gsh.getDataframe()
table_name = 'google_sheet_data'
users_df.to_sql(
    table_name,
    engine,
    if_exists='replace',
    index=False,
    chunksize=500,
    dtype={
        "Username": String(500),
        "Timezone": String(500),
        "UTC start": DateTime,
        "UTC end":  DateTime,
        "Number": String(500),
    }
)

table_df = pd.read_sql_table(
    table_name,
    con=engine
)

print(table_df.head())

# current_utc = datetime.datetime.utcnow()
# users_df["CreatedUTC"] = current_utc
"""
Why: there is a limit on the scalability of the architecture in the google spreadsheet. 

It is necessary to exclude all the code for working with Google spreadsheet and replace it with working with a database (PostgreSQL).
Prepare function Init which will automatically migrate data from the current table structure to a new one do not miss existing data.
As result, changes should make a backup of the data, create a new database with a new structure, and upload data from the backup.
"""
"""
# REMINDER: must share email located in key by pressing "share" button in google sheets to share with the credential email or it wont work!
"""
