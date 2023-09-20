from flask import Flask, render_template, request, redirect, url_for
from pymysql import connections
import os

app = Flask(__name__)

# MariaDB configuration
db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)

output = {}
table = 'lecturer'

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('lecturer.html')

@app.route("/EvaluateReport", methods=['GET', 'POST'])
def evaluate_report():
    if request.method == 'POST':
        # Assuming you have a form for report evaluation
        report_id = request.form['report_id']
        report_name = request.form['report_name']
        
        # Handle the report evaluation process here (e.g., download student report in PDF)
        # You need to specify the logic for downloading the report in PDF format
        # For demonstration purposes, we'll simulate it here:
        report_pdf_path = '/Downloads/' + report_name  # Replace with the actual path
        
        # Check if the file exists
        if os.path.exists(report_pdf_path):
            # Simulate sending the PDF for download
            return send_file(report_pdf_path, as_attachment=True)

    return render_template('EvaluateReport.html')

@app.route("/Grade", methods=['GET', 'POST'])
def grade_report():
    if request.method == 'POST':
        # Assuming you have multiple reports to grade
        report_id = request.form['report_id']  # Replace with the corresponding report_id
        student_score = request.form['student_score']  # Replace with the corresponding student_score

        # Now, you can insert the report_id and student_score into the database
        conn = db_conn.cursor()
        try:
            # Execute SQL statements to insert grading data into the database
            # Replace with your actual SQL query
            conn.execute("INSERT INTO grades (report_id, student_score) VALUES (?, ?)", (report_id, student_score))
            db_conn.commit()
            return "Report graded and data inserted into the database."
        except Exception as e:
            print(f"Error inserting grading data: {e}")
            return "An error occurred while processing the grading."

    return render_template('Grade.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
