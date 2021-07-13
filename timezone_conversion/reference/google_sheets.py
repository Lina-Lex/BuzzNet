import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# scope = [
#     'https://spreadsheets.google.com/spreadsheets',
#     'https://www.googleapis.com/auth/drive.file',
#     'https://www.googleapis.com/auth/drive'
# ]

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/batman/Desktop/googlesheets/key/master_key.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
#sheet = client.open('users_test')
#sheet = client.open('goanddo')

sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1gIDRAw203QCWp_8mGo6sZQi50vziKBsQShbd0txIktU/edit?usp=sharing")

# get the first sheet of the Spreadsheet
#sheet_instance = sheet.get_worksheet(0)
sheet_instance = sheet.worksheets()

print(type(sheet_instance))
print(sheet_instance)
print(dir(sheet_instance[0]))

dataframe = pd.DataFrame(sheet_instance[0].get_all_records())
print(dataframe.head())
