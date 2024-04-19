import sqlite3
import pandas as pd
import csv
import os

# CSV file paths
file1 = 'Datasets/Facility_Table_20240221.csv'
file2 = 'Datasets/Class_Data_Feb_21.csv'
file3 = 'Datasets/Master_Academic_Teaching_Spaces.csv'

db = sqlite3.connect('initial.db')

# Drop the CONSOLIDATED table if it exists
drop_table_consolidated = "DROP TABLE IF EXISTS CONSOLIDATED;"
db.execute(drop_table_consolidated)	

# Drop the C2 table if it exists
drop_table_C2 = "DROP TABLE IF EXISTS C2;"
db.execute(drop_table_C2)

# Drop the Spaces_Table table if it exists
drop_table_s_join = "DROP TABLE IF EXISTS Class_Data;"
db.execute(drop_table_s_join)

# Drop the Spaces_Table table if it exists
drop_table_s_join = "DROP TABLE IF EXISTS Facility_Table;"
db.execute(drop_table_s_join)

# Drop the Spaces_Table table if it exists
drop_table_s_join = "DROP TABLE IF EXISTS Spaces_Table;"
db.execute(drop_table_s_join)

# Pandas dataframe creation to read CSVs
directory = 'Datasets'
class_data = pd.read_csv(os.path.join(directory, 'Class_Data_Feb_21.csv'), encoding='latin1', low_memory=False)
facility_table = pd.read_csv(os.path.join(directory, 'Facility_Table_20240221.csv'), encoding='latin1', low_memory=False)
spaces_table = pd.read_csv(os.path.join(directory, 'Master_Academic_Teaching_Spaces.csv'), encoding='latin1', low_memory=False)

#Convert first 2 dataframes to sql tables
class_data.to_sql('Class_Data', db, if_exists='replace', index=False)
facility_table.to_sql('Facility_Table', db, if_exists='replace', index=False)

#SPACES TABLE PROCESSING: 
spaces_table.columns = spaces_table.columns.str.replace('#', '').str.replace('&\n','').str.replace(r'[\W_]+$', '', regex=True).str.replace(' ','_').str.replace('(','').str.replace('"','').str.replace('\n','')
spaces_table['BLDG_RM'] = spaces_table['BLDG_RM'].str.replace(' ', '')
spaces_table = spaces_table.rename(columns={'Room_Control_Systems_tech_that_controls_the_room': 'Room_Controls', 'ROOM_SIZESmall-under_40Medum-41-89Large-90-120X-Large-over_120': 'Room_Size', 'Room_Standards_HDMI,_Video,_Etc': 'Room_Standards', 'Room_Elements_Technology_in_the_Room' : 'Room_Elements'})

#Create a new column 'HDMI' based on the contents of 'Room_Standards'
spaces_table['HDMI'] = spaces_table['Room_Standards'].apply(lambda x: 'N' if pd.isna(x) else 'N' if 'No HDMI' in x else 'Y')

#Fill null values in 'HDMI' column with 'N'
#spaces_table['HDMI'] = spaces_table['HDMI'].fillna('N')

#Get the index of the 'Room_Standards' column
room_standards_index = spaces_table.columns.get_loc('Room_Standards')

#Insert the 'HDMI?' column right after the 'Room_Standards' column
spaces_table.insert(room_standards_index + 1, 'HDMI', spaces_table.pop('HDMI'))

#Convert to a SQL Table 
spaces_table.to_sql('Spaces_Table', db, if_exists='replace', index=False)




#CONSOLIDATION SCRIPT: Join the two tables on Facility_ID to create combined sheet

#Table creation, joining, and CLEANING: removing unneeded/redundant Fields
'''Excluded Columns/Fields: INSTRUCTION_MODE, c.MON, c.TUES, c.WED, c.THURS, c.FRI, c.SAT, c.SUN, c.MEETING_TIME_START, 
MEETING_TIME_END, INSTR_ASSIGN_SEQ, SETID, FACILITY_ID:1, EFFDT, EFF_STATUS, ROOM, DESCR:1,
c.FACILITY_GROUP, f.GENERL_ASSIGN, f.ACAD_ORG, f.FACILITY_PARTITION, f.MIN_UTLZN_PCT, f.LOCATION, 
EXT_SA_FACILITY_ID, f.FACILITY_CONFLICT'''

mk_consolidated = '''
    CREATE TABLE CONSOLIDATED AS
    SELECT
    
    c.CRSE_ID || '_' || c.CLASS_MTG_NBR || '_' || c.CRSE_OFFER_NBR || '_' || c.STRM || '_' || c.SESSION_CODE || '_' || c.CLASS_SECTION AS composite_key,
    c.CRSE_ID, c.CLASS_MTG_NBR, c.CRSE_OFFER_NBR, c.STRM, c.SESSION_CODE, c.SUBJECT, c.CATALOG_NBR, c.CLASS_SECTION, c.DESCR, 
    c.ENRL_TOT, c.INSTRUCTION_MODE_DESCR, c.FACILITY_ID, c.STND_MTG_PAT,
    c.START_TIME, c.END_TIME, c.START_DT, c.END_DT, c.EMPLID, c.INSTR_ROLE, c.FIRST_NAME, c.LAST_NAME, c.EMAIL_ADDR, 
    
    f.DESCRSHORT,f.FACILITY_TYPE, f.ROOM_CAPACITY, f.BLDG_CD
    

    FROM Class_Data AS c
    INNER JOIN Facility_Table AS f ON c.FACILITY_ID = f.FACILITY_ID
'''
db.execute(mk_consolidated)

#Academic Workspaces Consolidation
mk_C2 = '''
    CREATE TABLE C2 AS
    SELECT c.*, s.SFDB_CAP, s.Classroom_Furniture, s.Faculty_Furniture, s.Room_Controls, s.HDMI, s.Room_Standards, s.Room_Elements, s.Ad_Astra_Seats, s.IMS_Supported, s.Manager,  s.Manager_for_non_Uni_Rooms
    FROM CONSOLIDATED AS c
    LEFT JOIN Spaces_Table AS s ON
        CASE
            WHEN c.Facility_ID = 'ON' THEN 'ONLINE'  -- Mapping 'ON' to 'ONLINE'
            ELSE c.Facility_ID
        END = s.BLDG_RM;
'''
db.execute(mk_C2)

#Convert the C2 data to a CSV with Pandas - Download to project folder as 'C2.csv' and overwrites if any code changes
C2_data = pd.read_sql_query("SELECT * FROM C2", db)
C2_data.to_csv(os.path.join('CSVs', 'C2.csv'), index=False)


#Convert the Spaces data to a CSV with Pandas - Download to project folder as 'Spaces.csv' and overwrites if any code changes
Spaces_data = pd.read_sql_query("SELECT * FROM Spaces_Table", db)
Spaces_data.to_csv(os.path.join('CSVs', 'Cleaned_Spaces.csv'), index=False)

# Print column headers for CSV files
def print_column_headers(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Get the first row which contains the headers
        print("Column headers for", file_path, ":", headers)

# Print column headers for C2
print_column_headers(os.path.join('CSVs', 'C2.csv'))