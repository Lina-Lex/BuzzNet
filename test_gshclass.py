from util import *
import pytest
import os
from dotenv import load_dotenv

# creds
load_dotenv()
cred_path = os.environ.get("cred_json")

# testing constructor of GoogleSheetHelper class
def test_make_gsh_helper():
    gsh1 = GoogleSheetHelper(cred_path, "google_postgres", "existing")
    assert gsh1.cred_json == cred_path
    assert gsh1.spreadsheetName == "google_postgres"
    assert gsh1.sheetName == "existing"
    #assert type(gsh1.client) != type(gsh1.sheetName)

def test_columns_existing_tab():
    gsh_existing = GoogleSheetHelper(cred_path, "google_postgres", "existing")
    expected_columns = ['Phone Number', 'gender', 'dob', 'weight', 'height', 'activity',
       'hobby', 'time zone', 'call time', 'emergency phone', 'emergency name',
       'username', 'datetime added', 'friend', 'operator', 'type']
    assert len(gsh_existing.getDataframe().columns) == len(expected_columns)


def test_columns_calls_tab():
    gsh_calls = GoogleSheetHelper(cred_path, "google_postgres", "calls")
    expected_columns = ['Phone Number', 'gender', 'dob', 'weight', 'height', 'activity',
       'hobby', 'time zone', 'call time', 'emergency phone', 'emergency name',
       'username', 'datetime added', 'friend', 'operator', 'type']
    assert len(gsh_calls.getDataframe().columns) == len(expected_columns)


def test_columns_time_tab():
    gsh_time = GoogleSheetHelper(cred_path, "google_postgres", "time")
    expected_columns = ['Username', 'Timezone', 'UTC start', 'UTC end', 'Number']
    assert len(gsh_time.getDataframe().columns) == len(expected_columns)
