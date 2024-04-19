*** SJSUIT Data Processing & Upload Script ***

Requirements:
Python 3.8.8 or newer: https://www.python.org/downloads/
(Comes with SQLite and csv installed as standard libraries)

google_api_python_client==2.123.0
google_auth_oauthlib==1.2.0
pandas==2.0.3

1. Install Dependencies: (using pip installer)
pip install google-api-python-client==2.123.0 google-auth-oauthlib==1.2.0 pandas==2.0.3

2. Run initial.py Script: 2 ways
    1) With IDE like VSCode: open project folder and run initial.py
    2) Through Command Prompt/Terminal: 
        cd /path/sjsuIT/Scripts
        python initial.py

Upon Running:
- Datasets  consolidated
- Sqlite tables created
- Consolidated csv file C2.csv and cleaned dataset CSVs generated in CSVs folder

3. One-time Step: Configure Private Key for Google Drive API:
    1) Sign in to appropriate Google Account and go to Google Cloud Console: https://console.cloud.google.com
    2) Click Select Project (top left dropdown), and create new project, select it from the dropdown
    4) In above searchbar search and click on 'Google Drive API'
    5) Click Enable API and then Manage
    6) Click Configure Consent Screen and Select User Type - Internal for org access only and external for general access
    7) Make an app name and choose a support email and dev contact email, other fields are optional/as needed
    8) Save and Continue through the other steps and go back to dashboard when finished
    9) Click on OAuth consent screen and click 'Publish App'
    10) Go to Credentials, Create Credentials, OAuth Client ID, Choose Desktop App as Application Type, Any name, Click Create
    11) On OAuth client created screen, choose 'Download JSON'
    12) Rename the file as 'client_secret.json and place it in the Process_Upload_Script folder

4. Run gdrive.py Script: 2 ways
    1) Recommended - With IDE like VSCode: open project folder, open gdrive.py:
        One-time Step: Edit Target Folder ID: 
            Go to desired folder/location in Google Drive.
            Copy the last portion of the URL - part after "folders/"
            Paste it in the script: PARENT_FOLDER_ID = "<Your ID Here>"
    2) Through Command Prompt/Terminal: 
        cd /path/sjsuIT/Scripts
        python gdrive.py

Upon Running:
- Authentication flow starts: choose appropriate Google Account and Allow Permission --> Success message appears*
    - *If Authentication fails, close the script or press CTRL-C and rerun to authenticate again
- File is uploaded/updated to specified location in Google Drive and Terminal message states this

5. Open Tableau Desktop, select Google Drive as Data Source and navigate to C2.csv location, then authenticate

6. Dashboards and Visualizations appear - Changes to the dataset and rerunning 2 scripts as above updates the data and Tableau Dashboards

Additional:

To Edit the data and csv file or generate a new file: 
    Edit the initial.py script's SQL queries, rerun script, tables and files changed.
    Running gdrive.py updates files with the same name in the drive location, and creates them if they aren't made.

Pandas should be on the same PATH as Python interpreter. If issue appear, then try switching default Python interpreter.

'SQLite' extension for VSCode is helpful for quick viewing and querying the database tables.