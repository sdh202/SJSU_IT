*** Consolidation Script and In-Progess Use Case Analysis ***
Requirements:
google_api_python_client==2.123.0
google_auth_oauthlib==1.2.0
pandas==2.0.3
protobuf==5.26.1

1. Install Dependencies: (using pip installer)
pip install google-api-python-client==2.123.0 google-auth-oauthlib==1.2.0 pandas==2.0.3 protobuf==5.26.1

2. Run initial.py Script: 2 ways
    1) With IDE like VSCode: open project folder and run initial.py
    2) Through Command Prompt/Terminal: 
        cd /path/sjsuIT/Scripts
        python initial.py

Upon running:
- Datasets  consolidated
- Sqlite tables created
- Consolidated csv file C2.csv and cleaned dataset CSVs generated in CSVs folder.

3. Configure Private Key for Google Drive API - One time setup:
    1) Sign in to appropriate Google Account
    2) Go to Google Developer Console
    3) 

4. Run gdrive.py Script: 2 ways
    1) With IDE like VSCode: open project folder, open gdrive.py:
        Edit Target Folder ID: 
            Go to desired folder/location in Google Drive.
            Copy the last portion of the URL
            Paste it in the script: PARENT_FOLDER_ID = "<Your ID Here>"
    2) Through Command Prompt/Terminal: 
        cd /path/sjsuIT/Scripts
        python gdrive.py

5. Open Tableau Desktop and select Google Drive as Data Source and navigate to C2.csv location

6. Dashboards and Visualizations appear

Additional:
To Edit the data and csv file or generate a new file: 
    Edit the initial.py script's SQL queries, rerun script, tables and files changed.
    Running gdrive.py updates files with the same name, and creates them if they aren't made.





Diagram:


Notes:
Pandas should be on the same PATH as Python interpreter.
With above Requirements, initial.py can be run to generate
the sqlite 'initial' database with the sqlite tables.

'SQLite' extension for VSCode is helpful for quick viewing
and querying the database tables.

Google Drive Integration utilizes a google API with OAuth Authentication.
This requires generating and saving an API key from the Google Cloud Console 
into the project folder.
