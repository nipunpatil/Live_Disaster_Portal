import mysql.connector
from datetime import datetime

# Database configuration
db_config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'database': 'db1',
}

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

# Run the function
if __name__ == "__main__":
    delete_expired_rows()
