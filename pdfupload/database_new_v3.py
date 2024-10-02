# utils.py
import re
import os
from django.conf import settings
from django.db import connection, OperationalError
from django.core.files.storage import default_storage
from api.models import MtcV3

def read_column_names_from_file(filename):
    with open(filename, 'r') as file:
        column_names = file.read().splitlines()
    return column_names

def fetch_column_names():
    with connection.cursor() as cursor:
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'mtc_v3'")
        column_names = [row[0] for row in cursor.fetchall()]
    return column_names

def store_column_names_to_file(column_names, filename):
    with open(filename, 'w') as file:
        for column_name in column_names:
            file.write(column_name + '\n')

def compare_and_alter_table(current_column_names, stored_column_names):
    new_columns = set(current_column_names) - set(stored_column_names)
    print(f'-------------{new_columns}-----from missed column-------')
    if new_columns:
        with connection.cursor() as cursor:
            # Construct the ALTER TABLE query to add all missing columns
            alter_query = "ALTER TABLE mtc_v3 "
            alter_query += ", ".join([f"ADD COLUMN IF NOT EXISTS {column_name} VARCHAR(255)" for column_name in new_columns])

            # Execute the ALTER TABLE query
            cursor.execute(alter_query)
            connection.commit()

        # Update the stored column names in the text file
        stored_column_names.extend(new_columns)
        store_column_names_to_file(stored_column_names, 'column_names.txt')

def sanitize_string(s):
    # Replace spaces with underscores
    s = s.replace(' ', '_')
    # Remove special characters except underscores
    s = re.sub(r'[^\w\s]', '', s)
    return s

def get_list(list_rows):
    print(list_rows, '-----------')
    for i in range(0, len(list_rows), 2):
        try:
            # Combine column names from two lists
            column_names = list_rows[i][0] + list_rows[i+1][0][2:]
            column_names = ['che_' + sanitize_string(item.split(' ', 1)[0]) for item in column_names]
            for j in range(1, len(list_rows[i])):
                # Combine data from two lists
                combined_data = list_rows[i][j] + list_rows[i+1][j][2:]
                print('-----------------------------', 'rows')
                print(combined_data)
                print('---------column--------------------')
                column_check_database(column_names)
                print('-----------------------------')
                
                # Generate placeholders for the SQL query
                placeholders = ', '.join(['%s'] * len(combined_data))
                column_check_database(column_names)
                
                # Create or update the MtcV3 model instance
                values = dict(zip(column_names, combined_data))
                MtcV3.objects.create(**values)
        except OperationalError as e:
            print("Notification: Column already exists. Continuing program execution.", f'--------{e}==exception=====')
        except Exception as e:
            print(f"An error occurred: line 103 {e}")
        except:
            print("code error / only single page available")
            print(list_rows)
            
def column_check_database(column_names_new):
    # Check if the column_names.txt file exists
    if os.path.exists('column_names.txt'):
        # Read stored column names from the text file
        stored_column_names = read_column_names_from_file('column_names.txt')
       
        # Fetch current column names from the database
        current_column_names = column_names_new  # fetch_column_names(cur)

        # Compare current and stored column names and alter table if necessary
        compare_and_alter_table(current_column_names, stored_column_names)
    else:
        # Fetch current column names from the database
        current_column_names = fetch_column_names()
        # Store current column names to a text file
        store_column_names_to_file(current_column_names, 'column_names.txt')
        stored_column_names = read_column_names_from_file('column_names.txt')

        # Fetch current column names from the database
        current_column_names = column_names_new  # fetch_column_names(cur)

        # Compare current and stored column names and alter table if necessary
        compare_and_alter_table(current_column_names, stored_column_names)
