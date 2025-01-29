from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# ✅ Function to get MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="sourabh",  # Replace with your actual MySQL password
        database="attendance_management"
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/attendance')
def attendance():
    """ Fetch all attendance records from MySQL """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM attendance")
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('attendance.html', records=records)

@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    """ Add new attendance record to MySQL """
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        attendance_date = request.form['attendance_date']
        attendance_status = request.form['attendance_status']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # ✅ Insert query for adding records
            insert_query = """
                INSERT INTO attendance (student_id, course_id, attendance_date, attendance_status)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (student_id, course_id, attendance_date, attendance_status))

            connection.commit()  # ✅ Commit transaction
            cursor.close()
            connection.close()

            return redirect(url_for('attendance'))
        except Exception as e:
            return f"Error: {e}"  # Return error message for debugging

    return render_template('add_attendance.html')

if __name__ == '__main__':
    app.run(debug=True)
