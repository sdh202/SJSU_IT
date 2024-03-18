import sqlite3
import pandas as pd

# CSV file paths
file1 = 'Facility_Table_20240221.csv'
file2 = 'Class_Data_Feb_21.csv'
file3 = 'Master_Academic_Teaching_Spaces.csv'

# Create initial db and convert CSVs into SQL Tables
'''
TODO: Move to MySQL and add in dependencies for provisioning SQL server.
- Credentials
- Port on which server is open
'''
db = sqlite3.connect('initial.db')

#TODO: Code Numbering

#Pandas dataframe creation to read CSVs
class_data = pd.read_csv('Class_Data_Feb_21.csv', encoding='latin1', low_memory=False)
facility_table = pd.read_csv('Facility_Table_20240221.csv', encoding='latin1', low_memory=False)

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
'''