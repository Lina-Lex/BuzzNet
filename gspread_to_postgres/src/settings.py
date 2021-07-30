import os
from .coresettings import Checksettings


####### Define Your settings Below ############


class Spreadsheet_config(Checksettings):
 
    credential_path = os.environ['JSON_OAUTH_PATH']
    spreadsheet_name = "google_postgres"
    backup_all_worksheets = True     
    worksheet_to_consider = []         # should be emtry if backup_all_worksheet is True


class PostgresSQL_config(Checksettings):

    DRIVER = "postgresql"  # Dont change this ,Not recomended
    host = os.environ.get("PSQL_HOST","localhost")
    port = os.environ.get("PSQL_PORT",5432)
    username = os.environ.get("PSQL_USERNAME","postgres")
    password = os.environ.get("PSQL_PASSWORD","password123")

    # uncommenct and specify .DB name will automatically be fetched from spreadsheetName if not given
    # database = None
