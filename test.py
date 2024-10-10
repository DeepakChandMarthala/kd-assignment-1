import mysql.connector

DB_CONFIG = {
    'user': 'myuser',
    'password': 'myuser',
    'host': '34.130.62.29',  # Cloud SQL instance public IP
    'port': 3306,
    'database': 'myvalues'
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print("Successfully connected to the database")
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, registration_number) VALUES ('Test User', '12345')")
    conn.commit()
    
    print("Data inserted successfully!")
    
    cursor.close()
    conn.close()
except mysql.connector.Error as err:
    print(f"Error: {str(err)}")
