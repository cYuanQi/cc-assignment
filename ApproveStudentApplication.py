# Import additional modules
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

# Route for updating student information and retrieving resumes
@app.route("/update_student", methods=["POST"])
def update_student():
    # Get student information from the form
    student_id = request.form["student_id"]
    student_name = request.form["student_name"]
    field_of_study = request.form["field_of_study"]
    level_of_study = request.form["level_of_study"]

    # Update the student information in the database
    cursor = db_conn.cursor()
    update_sql = "UPDATE student_table SET student_name=%s, field_of_study=%s, level_of_study=%s WHERE student_id=%s"
    cursor.execute(update_sql, (student_name, field_of_study, level_of_study, student_id))
    db_conn.commit()
    cursor.close()

    # Retrieve the resume from Amazon S3
    # Retrieve the resume from Amazon S3
    resume_file_name = f"resume{student_id}.pdf"
    s3 = boto3.client('s3')
    try:
        s3_object = s3.get_object(Bucket=bucket, Key=resume_file_name)  # Use the 'bucket' variable
        resume_data = s3_object['Body'].read()
    except Exception as e:
        return str(e)  # Handle S3 retrieval error


    # Redirect to the page where you display the updated student information and resume
    return redirect(url_for("display_student", student_id=student_id))

# Route for displaying the student information and resume
@app.route("/display_student/<student_id>")
def display_student(student_id):
    # Query the database to get the student information
    cursor = db_conn.cursor()
    select_sql = "SELECT * FROM student_table WHERE student_id=%s"
    cursor.execute(select_sql, student_id)
    student_info = cursor.fetchone()
    cursor.close()

    # Render a template to display the student information and resume
    return render_template("student_template.html", student=student_info)



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
