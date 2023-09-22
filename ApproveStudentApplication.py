## Import additional modules
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

# MySQL database connection setup
db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('CompanyConfStudApp.html')


@app.route("/CompanyConfStudApp", methods=['GET', 'POST'])
def CompanyConfStudApp():
    return render_template('CompanyConfStudApp.html')

@app.route("/company", methods=['GET', 'POST'])
def company():
    return render_template('company.html')

# Route for approving a student and inserting into the database
@app.route("/approve_student", methods=["POST"])
def approve_student():
    # Predefined values for student
    student_id = 1  # You can set the student_id to the appropriate value
    student_name = "Student 1"
    field_of_study = "Computer Science"
    level_of_study = "Degree"

    # Insert the student's details into the database (e.g., approved_students table)
    cursor = db_conn.cursor()
    insert_sql = "INSERT INTO approved_students(student_id, student_name, field_of_study, level_of_study) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_sql, (student_id, student_name, field_of_study, level_of_study))
    db_conn.commit()
    cursor.close()

 
    flash("Student approved successfully!", "success")

    # Render the same template with the success message
    return render_template('CompanyConfStudApp.html')

@app.route("/display_approved_student/<student_id>")
def display_approved_student(student_id):
    # Query the database to get the approved student's information
    cursor = db_conn.cursor()
    select_sql = "SELECT * FROM approved_students WHERE student_id=%s"
    cursor.execute(select_sql, student_id)
    student_info = cursor.fetchone()
    cursor.close()

    # Render a template to display the approved student's details
    return render_template("approved_student_template.html", student=student_info)


@app.route("/nologin")
def nologin():
    return render_template('no_login.html')
    
@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/joblistings")
def joblistings():
    return render_template('job-listings.html')

@app.route("/jobsingle")
def jobsingle():
    return render_template('job-single.html')

@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/servicesingle")
def servicesingle():
    return render_template('service-single.html')

@app.route("/blog")
def blog():
    return render_template('blog.html')

@app.route("/blogsingle")
def blogsingle():
    return render_template('blog-single.html')

@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')

@app.route("/portfoliosingle")
def portfoliosingle():
    return render_template('portfolio-single.html')

@app.route("/testimonials")
def testimonials():
    return render_template('testimonials.html')

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/gallery")
def gallery():
    return render_template('gallery.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/studentApplication")
def student_application():
    return render_template('CompanyConfStudApp.html')


@app.route("/postjob")
def postjob():
    return render_template('post-job.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
