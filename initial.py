import sqlite3
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os

# CSV file paths
file1 = 'Datasets/Facility_Table_20240221.csv'
file2 = 'Datasets/Class_Data_Feb_21.csv'
file3 = 'Datasets/Master_Academic_Teaching_Spaces.csv'

db = sqlite3.connect('initial.db')

#TODO: Code Numbering

#Pandas dataframe creation to read CSVs
class_data = pd.read_csv('Datasets/Class_Data_Feb_21.csv', encoding='latin1', low_memory=False)
facility_table = pd.read_csv('Datasets/Facility_Table_20240221.csv', encoding='latin1', low_memory=False)

class_data.to_sql('Class_Data', db, if_exists='replace', index=False)
facility_table.to_sql('Facility_Table', db, if_exists='replace', index=False)

#CONSOLIDATION SCRIPT: Join the two tables on Facility_ID to create combined sheet

# Drop the Consolidated table if it exists
drop_table_query = "DROP TABLE IF EXISTS CONSOLIDATED;"
db.execute(drop_table_query)

#Table creation, joining, and CLEANING: removing unneeded/redundant Fields
'''Excluded Columns/Fields: c.CRSE_OFFER_NBR, c.SESSION_CODE, INSTRUCTION_MODE, CLASS_MTG_NBR, STND_MTG_PAT, MEETING_TIME_START, 
MEETING_TIME_END, INSTR_ASSIGN_SEQ, SETID, FACILITY_ID:1, EFFDT, EFF_STATUS, BLDG_CD, ROOM, DESCR:1,
c.FACILITY_GROUP, f.GENERL_ASSIGN, f.ACAD_ORG, f.FACILITY_PARTITION, f.MIN_UTLZN_PCT, f.LOCATION, 
EXT_SA_FACILITY_ID, f.FACILITY_CONFLICT'''

mk_consolidated = '''
    CREATE TABLE CONSOLIDATED AS
    SELECT c.CRSE_ID, c.SUBJECT, c.CATALOG_NBR, c.CLASS_SECTION, c.DESCR, 
    c.ENRL_TOT, c.INSTRUCTION_MODE_DESCR, c.FACILITY_ID, c.MON, c.TUES, c.WED, c.THURS, c.FRI, c.SAT, c.SUN,
    c.START_TIME, c.END_TIME, c.EMPLID, c.INSTR_ROLE, c.FIRST_NAME, c.LAST_NAME, c.EMAIL_ADDR, f.DESCRSHORT,
    f.FACILITY_TYPE, f.ROOM_CAPACITY
    FROM Class_Data AS c
    INNER JOIN Facility_Table AS f ON c.FACILITY_ID = f.FACILITY_ID
'''
db.execute(mk_consolidated)

#Convert the Consolidated data to a CSV with Pandas - Download to project folder as 'consolidated_data.csv' and overwrites if any code changes
consolidated_data = pd.read_sql_query("SELECT * FROM CONSOLIDATED", db)
consolidated_data.to_csv('CSVs/consolidated_data.csv', index=False)


# Drop the ROOMCAP_Join table if it exists
drop_table_query = "DROP TABLE IF EXISTS ROOMCAP_Join;"
db.execute(drop_table_query)

# Extract new table with Room number and capacity from FID_Join
mk_roomcap_join = '''                    
                    CREATE TABLE ROOMCAP_Join AS
                    SELECT DISTINCT m.FACILITY_ID, m.DESCR, m.ROOM_CAPACITY
                    FROM CONSOLIDATED AS m
                    ORDER BY m.ROOM_CAPACITY DESC;
                    '''
db.execute(mk_roomcap_join)

# Drop the ROOMCAP_Join table if it exists
drop_table_query = "DROP TABLE IF EXISTS UC1_CLASSCOUNT;"
db.execute(drop_table_query)


#USE CASE 1: How many classes are scheduled in this room
# TODO: Tableau filters for individual room selection
mk_classcount_join = '''                    
                    CREATE TABLE UC1_CLASSCOUNT AS
                    SELECT DISTINCT m.FACILITY_ID, COUNT (m.CRSE_ID) AS ClassCount
                    FROM CONSOLIDATED AS m
                    GROUP BY m.FACILITY_ID
                    ORDER BY ClassCount DESC;
                    '''
db.execute(mk_classcount_join)

#Convert the Classcount data to a CSV with Pandas - Download to project folder as 'UC1_classcount.csv' and overwrites if any code changes
consolidated_data = pd.read_sql_query("SELECT * FROM CONSOLIDATED", db)
consolidated_data.to_csv('CSVs/UC1_classcount_data.csv', index=False)

#Google drive integration with oauth
SCOPES = ['https://www.googleapis.com/auth/drive']
PARENT_FOLDER_ID = "1ttQL9hPKe_kTvA7jeeuBvAEaJKF6FA61"

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

def upload_csv(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    file_name = os.path.basename(file_path)

    with open(file_path, 'r') as csv_file:
        csv_contents = pd.read_csv(file_path, encoding='latin1', low_memory=False)

    file_metadata = {
        'name' : file_name,
        'parents' : [PARENT_FOLDER_ID],
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }
    
    file = service.files().create(
        body = file_metadata,
        media_body=file_path
    ).execute()

upload_csv("CSVs/consolidated_data.csv")











'''FOR REFERENCE  
# Function to print column headers of a CSV file
def print_column_headers(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Get the first row which contains the headers
        print("Column headers for", file_path, ":", headers)

# Print column headers for CSV file 1
print_column_headers(file1)

# Print column headers for CSV file 2
print_column_headers(file2)        

#USE CASE: CAPACITY MANAGEMENT
#JOIN ON FACILITY_ID : IF file1.ROOM_CAPACITY > file2.ENRL_TOT --> Get file2.DESCR --> Print Descending

locationTest = 
CREATE TABLE LT AS
SELECT FACILITY_ID, LOCATION
FROM CONSOLIDATED
WHERE LOCATION != 'MAIN';

db.execute(locationTest)

#Google drive integration with service account
from google.oauth2 import service_account
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'
PARENT_FOLDER_ID = ""

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_csv(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    with open(file_path, 'r') as csv_file:
        csv_contents = pd.read_csv(file_path, encoding='latin1', low_memory=False)

    file_metadata = {
        'name' : "consolidated_data",
        'parents' : [PARENT_FOLDER_ID],
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }
    
    file = service.files().create(
        body = file_metadata,
        media_body=file_path
    ).execute()

upload_csv("CSVs/consolidated_data.csv")

'''