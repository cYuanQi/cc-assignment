from flask import Flask, render_template, request, redirect, url_for
import mariadb
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

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('lecturer.html')

@app.route("/evaluate_report", methods=['GET', 'POST'])
def evaluate_report():
    if request.method == 'POST':
        # Assuming you have a form for report evaluation
        report_id = request.form['report_id']
        # Handle the report evaluation process here (e.g., download student report in PDF)

        # For example, you can store the evaluation result in the database
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                # Execute SQL statements to insert evaluation data into the database
                # Replace with your actual SQL query
                cursor.execute("INSERT INTO evaluation (report_id, evaluation_result) VALUES (?, ?)", (report_id, "A"))
                conn.commit()
                cursor.close()
                conn.close()
                return "Report evaluated and data inserted into the database."
            except mariadb.Error as e:
                print(f"Error inserting evaluation data: {e}")
                return "An error occurred while processing the evaluation."

    return render_template('EvaluateReport.html')

@app.route("/grade_report", methods=['GET', 'POST'])
def grade_report():
    if request.method == 'POST':
        # Assuming you have a form for grading student reports
        report_id = request.form['report_id']
        student_score = request.form['student_score']
        # Handle the grading process here

        # For example, you can store the grading result in the database
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                # Execute SQL statements to insert grading data into the database
                # Replace with your actual SQL query
                cursor.execute("INSERT INTO grades (report_id, student_score) VALUES (?, ?)", (report_id, student_score))
                conn.commit()
                cursor.close()
                conn.close()
                return "Report graded and data inserted into the database."
            except mariadb.Error as e:
                print(f"Error inserting grading data: {e}")
                return "An error occurred while processing the grading."

    return render_template('Grade.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)