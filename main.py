"""
from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from google.cloud import storage
import os

# Initialize Flask app
app = Flask(__name__)

# Set up GCP MySQL connection
db_config = {
    'user': 'myuser',
    'password': 'myuser',
    'host': '34.130.62.29',  # Replace with your MySQL IP address
    'database': 'myvalues',
}

# GCP Bucket Name
bucket_name = 'kd-project-bucket'

# Configure GCP Storage"""
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\admin\Documents\Sem-3\karan-dhawan\kd-project-436123-80898d8a34af.json'
"""client = storage.Client()
bucket = client.bucket(bucket_name)

# Home route with form to add and fetch data
@app.route('/')
def index():
    return render_template('index.html', records=None, inserted_data=None)

# Insert data (name, registration) into MySQL
@app.route('/insert', methods=['POST'])
def insert_data():
    name = request.form['name']
    reg_number = request.form['reg_number']

    # Insert data into MySQL
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "INSERT INTO students (name, registration_number) VALUES (%s, %s)"
    cursor.execute(query, (name, reg_number))
    connection.commit()
    
    # Fetch inserted data
    cursor.execute("SELECT name, registration_number FROM students WHERE name = %s AND registration_number = %s", (name, reg_number))
    inserted_data = cursor.fetchone()
    
    cursor.close()
    connection.close()

    # Pass inserted data to the template
    return render_template('index.html', inserted_data=inserted_data, records=None)

# Fetch recently added data from MySQL
@app.route('/fetch')
def fetch_data():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT name, registration_number FROM students ORDER BY id DESC LIMIT 3"
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    connection.close()

    # Keep the inserted data when fetching
    inserted_data = request.args.get('inserted_data')

    return render_template('index.html', records=records, inserted_data=inserted_data)

# Upload file to GCP Bucket
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
"""

#################################
"""
from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector
from google.cloud import storage
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Set up GCP MySQL connection
db_config = {
    'user': 'myuser',
    'password': 'myuser',
    'host': '34.130.62.29',  # Replace with your MySQL IP address
    'database': 'myvalues',
}

# GCP Bucket Name
bucket_name = 'kd-project-bucket'

# Set Google Cloud credentials environment variable"""
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\admin\Documents\Sem-3\karan-dhawan\kd-project-436123-80898d8a34af.json'
"""
# Function to upload file to GCP Bucket
def upload_to_gcp_bucket(file):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file.filename)

    # Upload the file to GCP Bucket
    blob.upload_from_file(file)

    # Make the file publicly accessible (optional)
    # blob.make_public()

    return blob.public_url

# Home route with form to add and fetch data
@app.route('/')
def index():
    return render_template('index.html', records=None, inserted_data=None)

# Insert data (name, registration) into MySQL
@app.route('/insert', methods=['POST'])
def insert_data():
    name = request.form['name']
    reg_number = request.form['reg_number']

    # Insert data into MySQL
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "INSERT INTO students (name, registration_number) VALUES (%s, %s)"
    cursor.execute(query, (name, reg_number))
    connection.commit()
    
    # Fetch inserted data
    cursor.execute("SELECT name, registration_number FROM students WHERE name = %s AND registration_number = %s", (name, reg_number))
    inserted_data = cursor.fetchone()
    
    cursor.close()
    connection.close()

    # Pass inserted data to the template
    return render_template('index.html', inserted_data=inserted_data, records=None)

# Fetch recently added data from MySQL
@app.route('/fetch')
def fetch_data():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT name, registration_number FROM students ORDER BY id DESC LIMIT 3"
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    connection.close()

    # Keep the inserted data when fetching
    inserted_data = request.args.get('inserted_data')

    return render_template('index.html', records=records, inserted_data=inserted_data)

# Upload file to GCP Bucket
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        file_url = upload_to_gcp_bucket(file)
        flash(f'File uploaded successfully! URL: {file_url}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
"""




from flask import Flask, request, render_template, redirect, url_for, flash, session
import mysql.connector
from google.cloud import storage
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed to use session

# Set up GCP MySQL connection
db_config = {
    'user': 'myuser',
    'password': 'myuser',
    'host': '34.130.62.29',  # Replace with your MySQL IP address
    'database': 'myvalues',
}

# GCP Bucket Name
bucket_name = 'kd-project-bucket'

# Set Google Cloud credentials environment variable
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\admin\Documents\Sem-3\karan-dhawan\kd-project-436123-80898d8a34af.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/app/service-account.json'

# Function to upload file to GCP Bucket
def upload_to_gcp_bucket(file):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file.filename)

    # Upload the file to GCP Bucket
    blob.upload_from_file(file)

    return blob.public_url

# Home route with form to add and fetch data
@app.route('/')
def index():
    inserted_data = session.get('inserted_data')  # Retrieve inserted data from session
    records = session.get('records')  # Retrieve fetched records from session
    return render_template('index.html', records=records, inserted_data=inserted_data)

# Insert data (name, registration) into MySQL
@app.route('/insert', methods=['POST'])
def insert_data():
    name = request.form['name']
    reg_number = request.form['reg_number']

    # Insert data into MySQL
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "INSERT INTO students (name, registration_number) VALUES (%s, %s)"
    cursor.execute(query, (name, reg_number))
    connection.commit()
    
    # Fetch inserted data
    cursor.execute("SELECT name, registration_number FROM students WHERE name = %s AND registration_number = %s", (name, reg_number))
    inserted_data = cursor.fetchone()
    
    cursor.close()
    connection.close()

    # Store inserted_data in session
    session['inserted_data'] = inserted_data

    return redirect(url_for('index'))

# Fetch recently added data from MySQL
@app.route('/fetch')
def fetch_data():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT name, registration_number FROM students ORDER BY id DESC LIMIT 3"
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    connection.close()

    # Store the fetched records in session
    session['records'] = records

    return redirect(url_for('index'))

# Upload file to GCP Bucket
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        file_url = upload_to_gcp_bucket(file)
        flash(f'File uploaded successfully! URL: {file_url}')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
