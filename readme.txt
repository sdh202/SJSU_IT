*** Consolidation Script and In-Progess Use Case Analysis ***
Requirements (pipreqs): 
    pandas==2.0.3
    Requests==2.31.0

With above Requirements, initial.py can be run to generate
sqlite 'initial' database with the associated tables.

The 'Consolidated' master sheet with cleaned columns, as well
as the Use case 1 table: UC1_CLASSCOUNT are coverted to CSV files
upon running the script. They are updated if the code is modified.
The CSV's can be directly imported into Google Sheets.

Aim ahead is to incorporate and clean the 3rd
sheet: 'Master_Academic_Teaching_Spaces' into the Consolidated
table.