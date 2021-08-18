# Gspread_to_postgres

This program helps in backing up data from your google spreadsheet to PostgresSQL server .

Need to install ```python 3.7+``` , ```sqlalchemy```, ```gspread```, ```oauth2client``` for working.
Just ```pip install <package_name>```

## Settings ENV variables 

* All the settings are present in the ```src/settings.py``` file which can be changed according to the need
* List of environ variables used currently are listed below
    * JSON_OAUTH_PATH :- A Path where the json key is stored for connecting to google service account
    * PSQL_USERNAME:- your postgress username
    * PSQL_PASSWORD :- you postgress user password
    * PSQL_HOST :- postgres server hostname
    * PSQL_PORT :- postgres server port 

* ***Note these flags should be set in the os environment variable list***

### General usage ###
* The Program can be run directly via python cli or can be run in a cron or scheduler
* The main entrypoint for the program is the execute function defined inside the **google_sheets_to_postgres.py** file
* To run the program in python cli 

    * ``` python gspread_to_postgres ```

* To run as a cron or scheduler, just import the below frunction as shown and scheduler it to run periodically

    * ``` from gspread_to_postgres import execute ```

