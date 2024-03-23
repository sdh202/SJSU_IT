*** Consolidation Script and In-Progess Use Case Analysis ***
Requirements (pipreqs): 
google_api_python_client==2.123.0
google_auth_oauthlib==1.2.0
pandas==2.0.3

#TODO: Add more detailed guide and Google Drive Instructions

Pandas should be on the same PATH as Python interpreter.
With above Requirements, initial.py can be run to generate
the sqlite 'initial' database with the sqlite tables.

'SQLite' extension for VSCode is helpful for quick viewing
and querying the database tables.

The 'Consolidated' master sheet with cleaned columns, as well
as the Use case 1 table: UC1_CLASSCOUNT are coverted to CSV files
upon running the script, and are added to the CSVs folder. 
They are updated if the code is modified.
The CSV's can be directly imported into Google Sheets. 

Aim ahead is to incorporate and clean the 3rd
sheet: 'Master_Academic_Teaching_Spaces' into the Consolidated
table.