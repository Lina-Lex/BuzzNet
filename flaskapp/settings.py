import os

# ---------- Twilio configuration ------------------

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_MAIN_PHONE_NUMBER = os.environ.get("TWILIO_MAIN_PHONE_NUMBER", "") # main_number

# Optional phone number
TWILIO_OPT_PHONE_NUMBER = os.environ.get("TWILIO_OPT_PHONE_NUMBER", "") #optional_number


# ---------- Google API Configs --------------------

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

# Google custom search ID
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID", "")

# Max number of items to return when do searching
GOOGLE_CSE_MAX_NUM = 3

# Path to the json file with Google service account credentials
GOOGLE_SA_JSON_PATH = os.environ.get("GOOGLE_SA_JSON_PATH", "") # cred_json


# ---------- Google docs IDs -----------------------

GOOGLE_USERS_SPREADSHEET_NAME = "Users"
GOOGLE_USERS_SPREADSHEET_ID = ""
GOOGLE_USERS_SHEET_NAME_EXISTING = "Existing"
GOOGLE_USERS_SHEET_NAME_CALLS = "Calls"

GOOGLE_FEEDBACK_SPREADSHEET_NAME = "feedback"
GOOGLE_FEEDBACK_SPREADSHEET_ID = ""
GOOGLE_FEEDBACK_SHEET_NAME = "service"

GOOGLE_HEALTH_DB_SPREADSHEET_NAME = "health_metrics"
GOOGLE_HEALTH_DB_SPREADSHEET_ID = ""
GOOGLE_HEALTH_DB_SHEET_NAME = "blood_pressure"


# ------------ DATABASE CONFIGURATION --------------
POSTGRESQL_DB_NAME = 'goanddo'
POSTGRESQL_USER = 'postgres'
POSTGRESQL_PASSWORD = os.environ.get("POSTGRESQL_PASSWORD", "")
POSTGRESQL_HOST = '127.0.0.1'
POSTGRESQL_PORT = 5432

# Heroku specific settings
POSTGRESQL_URL = os.environ.get("POSTGRESQL_URL", "")
# --------------------------------------------------

# -----------  Helper constants --------------------
# True if we run the script on Heroku, otherwise False.
ON_HEROKU = 'HEROKU' in os.environ

# lst_num
ORDINAL_NUMBERS = [
    'first',
    'second',
    'third',
    'forth',
    'fifth',
    'sixth',
    'seventh',
    'eighth',
    'ninth',
    'tenth'
]

# -- Override some values for Heroku environment ---

#=====================
# if 'HEROKU' in os.environ:
#     import urllib.parse
#     import psycopg2
#     urllib.parse.uses_netloc.append('postgres')
#     url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
#     conn = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
#     db_proxy.initialize(conn)
# else:
#     conn = PostgresqlDatabase('goanddo', user='postgres', password=postgreSQLpass, host='127.0.0.1', port=5432)
#     db_proxy.initialize(conn)



# if 'HEROKU' in os.environ:
#     print ('nothing')
# else:
#     postgreSQLpass = os.environ['postgreSQLpass']



#import pprint
