from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pandas as pd
import csv

#TODO: Seperate google drive integration as being optional in a different script
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

def print_column_headers(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Get the first row which contains the headers
        print("Column headers for", file_path, ":", headers)