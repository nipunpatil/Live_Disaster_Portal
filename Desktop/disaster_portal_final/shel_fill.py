import pandas as pd
import mysql.connector
from mysql.connector import Error

# Function to create a database connection
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Define the columns to read
columns_to_read = [
    'SrNo', 
    'Health Facility Name', 
    'pincode', 
    'latitude', 
    'longitude', 
    'altitude', 
    'Facility Type', 
    'State_Name', 
    'District_Name', 
    'Taluka_Name'
]

# Read the CSV file and specify the columns
df = pd.read_csv('C:/Users/nipun/Downloads/shelters.csv', usecols=columns_to_read, dtype=str)
df.columns = df.columns.str.replace(' ', '_')  # Replace spaces in column names

# Debugging: Print DataFrame shape and columns
print("DataFrame shape:", df.shape)
print("Columns:", df.columns)

# Connect to MySQL
connection = create_connection("localhost", "root", "1234", "db1")

# Insert DataFrame records into MySQL
if connection is not None:
    cursor = connection.cursor()
    for index, row in df.iterrows():
        try:
            print(f"Inserting row {index}: {row}")  # Debugging: Print the row being inserted
            sql = """
            INSERT INTO shelter_shelter (sr_no, health_facility_name, pincode, latitude, longitude, altitude, facility_Type, state_Name, district_Name, taluka_Name) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, tuple(row))
        except Error as e:
            print(f"Error inserting row {index}: {e}")  # Print the error and continue with the next row
    
    # Commit the changes
    connection.commit()
    print(f"{cursor.rowcount} records inserted.")
    
    # Close the cursor and connection
    cursor.close()
    connection.close()
else:
    print("Connection to the database failed.")
