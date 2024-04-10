*** Consolidation Script and In-Progess Use Case Analysis ***
Requirements:
google_api_python_client==2.123.0
google_auth_oauthlib==1.2.0
pandas==2.0.3
protobuf==5.26.1

Notes:
Pandas should be on the same PATH as Python interpreter.
With above Requirements, initial.py can be run to generate
the sqlite 'initial' database with the sqlite tables.

'SQLite' extension for VSCode is helpful for quick viewing
and querying the database tables.

Google Drive Integration utilizes a google API with OAuth Authentication.
This requires generating and saving an API key from the Google Cloud Console 
into the project folder.