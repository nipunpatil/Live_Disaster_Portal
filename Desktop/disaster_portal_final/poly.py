import os
import mysql.connector
from mysql.connector import Error
import xml.etree.ElementTree as ET
from datetime import datetime

# Database configuration
db_config = {
    'host': 'localhost',  # Change if using a different host
    'user': 'root',  # Enter your MySQL username
    'password': '1234',  # Enter your MySQL password
    'database': 'db1'  # Enter your MySQL database name
}

# Function to connect to MySQL and insert data
def insert_into_db(data):
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # SQL insert query, including all the new parameters
        insert_query = '''
        INSERT INTO cap_alerts1 
        (identifier, sender, sent_time, status, msg_type, scope, category, event, urgency, certainty, effective, onset, expires, headline, description, polygon, area, severity)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        
        # Executing the query
        cursor.execute(insert_query, data)
        
        # Commit the transaction
        connection.commit()

        print(f"Data inserted successfully for identifier: {data[0]}")

    except Error as err:
        print(f"Error: {err}")
    
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

# Function to parse the file content as XML
def parse_oasis_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    namespace = {'cap': 'urn:oasis:names:tc:emergency:cap:1.2'}

    # Extracting the basic alert details
    identifier = root.find('cap:identifier', namespace).text
    sender = root.find('cap:sender', namespace).text
    sent_time = root.find('cap:sent', namespace).text
    status = root.find('cap:status', namespace).text
    msg_type = root.find('cap:msgType', namespace).text
    scope = root.find('cap:scope', namespace).text
    
    # Extracting the info block
    info = root.find('cap:info', namespace)
    category = info.find('cap:category', namespace).text
    event = info.find('cap:event', namespace).text
    urgency = info.find('cap:urgency', namespace).text
    certainty = info.find('cap:certainty', namespace).text
    effective = info.find('cap:effective', namespace).text
    onset = info.find('cap:onset', namespace).text if info.find('cap:onset', namespace) is not None else None
    expires = info.find('cap:expires', namespace).text
    headline = info.find('cap:headline', namespace).text
    description = info.find('cap:description', namespace).text if info.find('cap:description', namespace) is not None else None
    severity = info.find('cap:severity', namespace).text if info.find('cap:severity', namespace) is not None else None
    
    # Extracting the area block
    area = info.find('cap:area', namespace)
    area_desc = area.find('cap:areaDesc', namespace).text
    polygon = area.find('cap:polygon', namespace).text if area.find('cap:polygon', namespace) is not None else None

    # Return all data as a tuple
    return (identifier, sender, sent_time, status, msg_type, scope, category, event, urgency, certainty, effective, onset, expires, headline, description, polygon, area_desc, severity)

# Function to loop through all "file" type files in the downloaded_files folder
def process_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Open the file and check if it contains XML-like structure
        if os.path.isfile(file_path):
            print(f"Processing file: {filename}")
            try:
                data_to_insert = parse_oasis_xml(file_path)
                insert_into_db(data_to_insert)
            except ET.ParseError:
                print(f"File {filename} could not be parsed as XML.")
            except Exception as e:
                print(f"An error occurred while processing {filename}: {e}")

# Function to delete expired rows from the database
def delete_expired_rows():
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Get the current time
        current_time = datetime.now()

        # Define the query to delete expired rows
        delete_query = "DELETE FROM cap_alerts1 WHERE expires < %s"
        
        # Execute the delete query
        cursor.execute(delete_query, (current_time,))
        
        # Commit the changes
        connection.commit()

        print(f"Deleted {cursor.rowcount} expired row(s).")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# Main execution starts here
if __name__ == '__main__':
   
    
    folder_path = 'C:/Users/nipun/Desktop/new_se/downloaded_files'
    process_files_in_folder(folder_path)
    delete_expired_rows()