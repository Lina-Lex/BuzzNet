from util import *
import pytest
import os

# creds
cred_json = os.environ.get("json_path")

# testing constructor of GoogleSheetHelper class
def test_make_gsh_helper():
    gsh1 = GoogleSheetHelper(cred_json, "google_postgres", "existing")
    assert gsh1.cred_json == cred_json
    assert gsh1.spreadsheetName == "google_postgres"
    assert gsh1.sheetName == "existing"

def test_columns_existing_tab():
    gsh_existing = GoogleSheetHelper(cred_json, "google_postgres", "existing")
    expected_columns = ['Phone Number', 'gender', 'dob', 'weight', 'height', 'activity',
       'hobby', 'time zone', 'call time', 'emergency phone', 'emergency name',
       'username', 'datetime added', 'friend', 'operator', 'type']
    assert len(gsh_existing.getDataframe().columns) == len(expected_columns)

def test_columns_calls_tab():
    gsh_calls = GoogleSheetHelper(cred_json, "google_postgres", "calls")
    expected_columns = ['Phone Number', 'gender', 'dob', 'weight', 'height', 'activity',
       'hobby', 'time zone', 'call time', 'emergency phone', 'emergency name',
       'username', 'datetime added', 'friend', 'operator', 'type']
    assert len(gsh_calls.getDataframe().columns) == len(expected_columns)

def test_columns_time_tab():
    gsh_time = GoogleSheetHelper(cred_json, "google_postgres", "time")
    expected_columns = ['Username', 'Timezone', 'UTC start', 'UTC end', 'Number']
    assert len(gsh_time.getDataframe().columns) == len(expected_columns)
