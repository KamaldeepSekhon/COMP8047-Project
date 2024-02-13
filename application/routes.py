from application import app
from flask import render_template, request
import pyodbc 
import pandas as pd
import os
import warnings
import csv
warnings.filterwarnings("ignore")

conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-0F1D2L8;"
                      "Database=Major Project;"
                      "Trusted_Connection=yes;")

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", index=True)

@app.route("/courses")
def courses():
    courseData = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]
    print(courseData[0]["title"])
    return render_template("courses.html", courseData=courseData, courses = True )

@app.route("/register")
def register():
    return render_template("register.html", register=True)

@app.route("/login")
def login():
    return render_template("login.html", login=True)

# @app.route("/login")
# def login():
#     return render_template("login.html", login=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded files
        file_x = request.files['file_x']
        file_y = request.files['file_y']

        # Save the uploaded files
        file_x_path = os.path.join('uploads', file_x.filename)
        file_y_path = os.path.join('uploads', file_y.filename)
        file_x.save(file_x_path)
        file_y.save(file_y_path)


 # Open the CSV files and read data
 # Open the CSV files and read data
    with open(file_x_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        column_names = next(csv_reader)
        print(column_names)

        # Construct the SQL query to create the table
        cleaned_column_names = [col.strip().strip('"ï»¿') for col in column_names]
        create_table_query = f"CREATE TABLE tablex (id INT IDENTITY(1,1) PRIMARY KEY,{', '.join([f'{col.strip()} VARCHAR(20)' for col in cleaned_column_names])})"

        print("SQL Query:", create_table_query)  # Debugging statement

        # Establish a connection to the SQL Server


        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Execute the SQL query to create the table
        cursor.execute(create_table_query)

        for row in csv_reader:
            # Construct the INSERT INTO query
            insert_query = f"""
            INSERT INTO tablex ({', '.join(cleaned_column_names)})
            VALUES ({', '.join([f"'{val.strip()}'" for val in row])})
            """
            # Execute the INSERT INTO query
            cursor.execute(insert_query)


    with open(file_y_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        column_names = next(csv_reader)
        print(column_names)

        # Construct the SQL query to create the table
        cleaned_column_names = [col.strip().strip('"ï»¿') for col in column_names]
        create_table_query = f"CREATE TABLE tabley (id INT IDENTITY(1,1) PRIMARY KEY,{', '.join([f'{col.strip()} VARCHAR(20)' for col in cleaned_column_names])})"

        # print("SQL Query:", create_table_query) 
        cursor = conn.cursor()

        # Execute the SQL query to create the table
        cursor.execute(create_table_query)

        for row in csv_reader:
            # Construct the INSERT INTO query
            insert_query = f"""
            INSERT INTO tabley ({', '.join(cleaned_column_names)})
            VALUES ({', '.join([f"'{val.strip()}'" for val in row])})
            """
            # Execute the INSERT INTO query
            cursor.execute(insert_query)

    

    cursor.execute("SELECT * FROM tablex")
    columns_x = [column[0] for column in cursor.description]
    data_x = cursor.fetchall()

    # Fetch data from tabley
    cursor.execute("SELECT * FROM tabley")
    columns_y = [column[0] for column in cursor.description]
    data_y = cursor.fetchall()

    # Render the template and pass the data to it
    
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('viewdata.html', columns_x=columns_x, data_x=data_x, columns_y=columns_y, data_y=data_y)
    # return 'Files uploaded and data inserted into the database successfully.'

# if __name__ == '__main__':
#   app.run(debug=True)



