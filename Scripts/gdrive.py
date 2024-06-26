import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google drive integration with oauth
SCOPES = ['https://www.googleapis.com/auth/drive']
PARENT_FOLDER_ID = "<Your ID Here>"

def authenticate():
  flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
  creds = flow.run_local_server(port=0)
  return creds

def upload_csv(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    file_name = os.path.basename(file_path)

    # Prepare the metadata for the new Google Sheet
    new_sheet_metadata = {
        'name': file_name,
        'parents': [PARENT_FOLDER_ID],
        'mimeType': 'text/csv'
    }

    # Look for existing files with the same name in the parent folder
    query = f"name='{file_name}' and '{PARENT_FOLDER_ID}' in parents and trashed=false"
    existing_files = service.files().list(q=query, supportsAllDrives=True, includeItemsFromAllDrives=True).execute().get('files', [])

    if existing_files:
        existing_file_id = existing_files[0]['id']
        print("Existing files:", existing_files)  # Add this line to print existing files

        # Upload the new content as an update
        media = MediaFileUpload(file_path, mimetype='text/csv')
        updated_file = service.files().update(
            fileId=existing_file_id,
            media_body=media,
            supportsAllDrives=True
        ).execute()

        print(f"File '{file_name}' updated successfully.")
    else:
        # If the file doesn't exist, upload it as a new Google Sheet
        media = MediaFileUpload(file_path, mimetype='text/csv')
        file = service.files().create(
            body=new_sheet_metadata,
            media_body=media,
            supportsAllDrives=True
        ).execute()

        print(f"File '{file_name}' uploaded successfully.")

upload_csv("CSVs/C2.csv")