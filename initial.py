import csv
import sqlite3
import pandas as pd
''' RANDOM JUNK FOR REFERENCE  
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
'''
#random empty table creation test
#with open(file1, 'r') as file:
#    db.execute('''CREATE TABLE IF NOT EXISTS Facility_Tabl (
#                    FACILITY_ID INTEGER PRIMARY KEY,
#                    ROOM_CAPACITY INTEGER
#                )''')


# CSV file paths
file1 = 'Facility_Table_20240221.csv'
file2 = 'Class_Data_Feb_21.csv'

# Create initial db and convert CSVs into SQL Tables
db = sqlite3.connect('initial.db')

class_data = pd.read_csv('Class_Data_Feb_21.csv', encoding='latin1', low_memory=False)
facility_table = pd.read_csv('Facility_Table_20240221.csv', encoding='latin1', low_memory=False)

class_data.to_sql('Class_Data', db, if_exists='replace', index=False)
facility_table.to_sql('Facility_Table', db, if_exists='replace', index=False)

#Join the two tables on Facility_ID to create combined sheet
mk_fid_join = '''
    CREATE TABLE IF NOT EXISTS FID_Join AS
    SELECT *
    FROM Class_Data AS c
    INNER JOIN Facility_Table AS f ON c.FACILITY_ID = f.FACILITY_ID
'''
db.execute(mk_fid_join)

## TODO: FID_Join TABLE CLEANING with Pandas

# Drop the ROOMCAP_Join table if it exists
drop_table_query = "DROP TABLE IF EXISTS ROOMCAP_Join;"
db.execute(drop_table_query)

# Extract new table with Room number and capacity from FID_Join
mk_roomcap_join = '''                    
                    CREATE TABLE ROOMCAP_Join AS
                    SELECT DISTINCT m.FACILITY_ID, m.DESCR, m.ROOM_CAPACITY
                    FROM FID_Join AS m
                    ORDER BY m.ROOM_CAPACITY DESC;
                    '''
db.execute(mk_roomcap_join)

# Drop the ROOMCAP_Join table if it exists
drop_table_query = "DROP TABLE IF EXISTS CLASSCOUNT;"
db.execute(drop_table_query)

#USE CASE: How many classes in each room
mk_classcount_join = '''                    
                    CREATE TABLE CLASSCOUNT AS
                    SELECT DISTINCT m.FACILITY_ID, COUNT (m.CRSE_ID) AS ClassCount
                    FROM FID_Join AS m
                    GROUP BY m.FACILITY_ID
                    ORDER BY ClassCount DESC;
                    '''
db.execute(mk_classcount_join)