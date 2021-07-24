# util.py imports
import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, String, DateTime
import datetime
from dotenv import load_dotenv

# creds
load_dotenv()
cred_path = os.environ.get("cred_json")

class GoogleSheetHelper:
    """Helper claas to pull data from googlesheets"""
    def __init__(self, cred_json, spreadsheetName, sheetName):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.cred_json = cred_json
        self.spreadsheetName = spreadsheetName
        self.sheetName = sheetName
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.cred_json, self.scope)
        self.client = gspread.authorize(self.creds)

    def getDataframe(self):
        """Returns all rows data from sheet as dataframe"""
        spreadsheet = self.client.open(self.spreadsheetName)
        sheet = spreadsheet.worksheet(self.sheetName)
        rows = sheet.get_all_records()
        return pd.DataFrame(rows)

    def getDict(self):
        """Returns all rows data from sheet as dictionary--one dict per row"""        
        spreadsheet = self.client.open(self.spreadsheetName)
        sheet = spreadsheet.worksheet(self.sheetName)
        rows = sheet.get_all_records()
        return rows

    def viewAllClientSheets(self):
        """Returns sheets this gspread (self.client) authorized to view/edit"""
        available_sheets = self.client.openall()
        return [sheet.title for sheet in available_sheets]

# gsh1 = GoogleSheetHelper(cred_path, "google_postgres", "existing")
# print(type(gsh1))

gsh1 = GoogleSheetHelper(cred_path, "google_postgres", "time")
print(gsh1.getDataframe().columns)