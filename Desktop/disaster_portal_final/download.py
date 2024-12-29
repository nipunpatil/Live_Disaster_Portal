import feedparser
import requests
import os
import re
import time
from requests.exceptions import ChunkedEncodingError, RequestException
import mysql.connector
from mysql.connector import Error
import xml.etree.ElementTree as ET
from datetime import datetime

# Database configuration
db_config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'database': 'db1',
}

def sanitize_filename(filename):
    """Sanitize filenames to remove or replace invalid characters."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def get_current_urls(feed_url):
    """Fetch URLs from the RSS feed."""
    d = feedparser.parse(feed_url)
    urls = set()
    for entry in d.entries:
        links = entry.links
        for link in links:
            urls.add(link.href)
    return urls

def download_file(url, download_folder, max_retries=3, chunk_size=102400):
    """Download a file from a URL to a specified folder in chunks."""
    file_name = sanitize_filename(url.split('/')[-1])
    file_path = os.path.join(download_folder, file_name)
    retry_count = 0
    headers = {}

    while retry_count < max_retries:
        try:
            if os.path.exists(file_path):
                print(f"File {file_name} already exists. Skipping download.")
                return file_path  # File already downloaded

            response = requests.get(url, headers=headers, stream=True, timeout=10)

            if response.status_code in (200, 206):  # 200 OK, 206 Partial Content
                with open(file_path, 'wb') as file:
                    total_downloaded = 0
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            file.write(chunk)
                            total_downloaded += len(chunk)
                            print(f"Downloaded {total_downloaded} bytes of {file_name}")

                print(f"Downloaded {url} and saved as {file_name}")
                return file_path
            else:
                print(f"Failed to download {url}: Status code {response.status_code}")
                retry_count += 1

        except (ChunkedEncodingError, RequestException) as e:
            print(f"Error downloading {url}: {e}. Retrying... ({retry_count + 1}/{max_retries})")
            retry_count += 1

    print(f"Failed to download {url} after {max_retries} retries.")
    return None

def delete_expired_rows():
    """Delete expired rows from the database, keeping only unique identifiers."""
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        current_time = datetime.now()

        # Delete rows that have expired
        delete_expired_query = "DELETE FROM cap_alerts1 WHERE expires < %s"
        cursor.execute(delete_expired_query, (current_time,))
        connection.commit()
        print(f"Deleted {cursor.rowcount} expired row(s).")

        # Identify duplicate identifiers and keep only one instance of each
        delete_duplicates_query = '''
            DELETE FROM cap_alerts1 
            WHERE id NOT IN (
                SELECT id FROM (
                    SELECT MIN(id) AS id 
                    FROM cap_alerts1 
                    GROUP BY identifier
                ) AS temp
            )
        '''
        cursor.execute(delete_duplicates_query)
        connection.commit()
        print(f"Deleted duplicate entries for identifiers.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()



def insert_into_db(data):
    """Insert data into the MySQL database, only if it doesn't already exist."""
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if the identifier already exists
        check_query = "SELECT COUNT(*) FROM cap_alerts1 WHERE identifier = %s"
        cursor.execute(check_query, (data[0],))
        exists = cursor.fetchone()[0] > 0

        if exists:
            print(f"Data for identifier {data[0]} already exists. Skipping insert.")
            return  # Skip if the data already exists

        insert_query = '''
        INSERT INTO cap_alerts1 
        (identifier, sender, sent_time, status, msg_type, scope, category, event, urgency, certainty, effective, onset, expires, headline, description, polygon, area, severity)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        
        cursor.execute(insert_query, data)
        connection.commit()

        print(f"Data inserted successfully for identifier: {data[0]}")

    except Error as err:
        print(f"Error: {err}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def parse_oasis_xml(file_path):
    """Parse the XML file and extract relevant data."""
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

    return (identifier, sender, sent_time, status, msg_type, scope, category, event, urgency, certainty, effective, onset, expires, headline, description, polygon, area_desc, severity)

def process_files_in_folder(folder_path):
    """Process all XML files in the specified folder."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            print(f"Processing file: {filename}")
            try:
                data_to_insert = parse_oasis_xml(file_path)
                insert_into_db(data_to_insert)
            except ET.ParseError:
                print(f"File {filename} could not be parsed as XML.")
            except Exception as e:
                print(f"An error occurred while processing {filename}: {e}")

def main():
    feed_url = "https://sachet.ndma.gov.in/cap_public_website/rss/rss_india.xml"
    download_folder = 'downloaded_files'
    
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Load already downloaded files from a file, if it exists
    if os.path.exists('downloaded_files.txt'):
        with open('downloaded_files.txt', 'r') as f:
            downloaded_files = set(f.read().splitlines())
    else:
        downloaded_files = set()

    while True:
        current_urls = get_current_urls(feed_url)

        # Check and download new files
        for url in current_urls:
            file_name = sanitize_filename(url.split('/')[-1])
            if file_name not in downloaded_files:  # Check if the file has been downloaded
                file_path = download_file(url, download_folder)
                if file_path:  # If the file was successfully downloaded
                    with open('downloaded_files.txt', 'a') as f:
                        f.write(file_name + '\n')  # Save the filename

        # Process files in the downloaded folder
        process_files_in_folder(download_folder)

        # Delete expired rows
        delete_expired_rows()

        time.sleep(300)  # Check for new URLs every 30 seconds

if __name__ == "__main__":
    main()
