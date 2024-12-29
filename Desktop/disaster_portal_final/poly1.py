import os
import mysql.connector
from mysql.connector import Error
import xml.etree.ElementTree as ET

# Function to connect to MySQL and insert data
def insert_into_db(data):
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change if using a different host
            user='root',  # Enter your MySQL username
            password='1234',  # Enter your MySQL password
            database='db1'
        )
        cursor = connection.cursor()

        # SQL insert query
        insert_query = '''
        INSERT INTO cap_alerts1 
        (identifier, sender, sent_time, status, msg_type, scope, event, urgency, severity, certainty, headline, description, polygon, area)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

    identifier = root.find('cap:identifier', namespace).text
    sender = root.find('cap:sender', namespace).text
    sent_time = root.find('cap:sent', namespace).text
    status = root.find('cap:status', namespace).text
    msg_type = root.find('cap:msgType', namespace).text
    scope = root.find('cap:scope', namespace).text
    
    info = root.find('cap:info', namespace)
    event = info.find('cap:event', namespace).text
    urgency = info.find('cap:urgency', namespace).text
    severity = info.find('cap:severity', namespace).text
    certainty = info.find('cap:certainty', namespace).text
    headline = info.find('cap:headline', namespace).text
    description = info.find('cap:description', namespace).text
    
    area = info.find('cap:area', namespace)
    area_desc = area.find('cap:areaDesc', namespace).text
    polygon = area.find('cap:polygon', namespace).text

    return (identifier, sender, sent_time, status, msg_type, scope, event, urgency, severity, certainty, headline, description, polygon, area_desc)

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

# Main execution starts here
if __name__ == '__main__':
    folder_path = 'C:/Users/nipun/Desktop/new_se/downloaded_files'
    process_files_in_folder(folder_path)
