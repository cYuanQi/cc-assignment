# Import additional modules
from flask import Flask, render_template, request, redirect, url_for, flash
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Replace with a secret key for flash messages

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
output = {}
table = 'student'

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('student-details.html')

# Allowed file extensions for resume uploads
ALLOWED_EXTENSIONS = {'pdf'}

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the student details form
@app.route("/student_details", methods=['GET'])
def student_details_form():
    return render_template('student_details.html')

# Route for submitting student data
@app.route("/submit_student", methods=['POST'])
def submit_student():
    if request.method == 'POST':
        student_name = request.form['student_name']
        student_email = request.form['student_email']
        student_programme = request.form['student_programme']
        student_skills = request.form['student_skills']
        resume_file = request.files['resume_file']

        # Check if a file is selected and has the allowed extension
        if resume_file and allowed_file(resume_file.filename):
            # Upload resume file to a directory (you can modify this path)
            resume_filename = os.path.join('uploads', resume_file.filename)
            resume_file.save(resume_filename)
        else:
            flash('Invalid resume file. Please upload a PDF file.', 'error')
            return redirect(url_for('student_details_form'))

        # Insert student data into the database
        cursor = db_conn.cursor()
        insert_sql = "INSERT INTO student (student_name, student_email, student_programme, student_skills, resume_url) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_sql, (student_name, student_email, student_programme, student_skills, resume_filename))
        db_conn.commit()
        cursor.close()

        flash('Student data saved successfully', 'success')

        # Redirect to the route that displays the inserted data
        return redirect(url_for('display_student_data'))

# Route to display the inserted student data
@app.route("/display_student_data", methods=['GET'])
def display_student_data():
    cursor = db_conn.cursor()
    select_sql = "SELECT * FROM student ORDER BY student_id DESC LIMIT 1"
    cursor.execute(select_sql)
    student_data = cursor.fetchone()
    cursor.close()

    return render_template('display_student_data.html', student_data=student_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


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

@app.route("/studentreport")
def studentreport():
    return render_template('Student_report.html')

@app.route("/studentdetails")
def studentdetails():
    return render_template('student-details.html')

@app.route("/userpage")
def userpage():
    return render_template('user_page.html')

@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/studentapplyjobs")
def studentapplyjobs():
    return render_template('StudentApplyJobs.html')

@app.route("/companylistadm")
def companylistadm():
    return render_template('company_list_adm.html')

@app.route("/assignsupervisor")
def assignsupervisor():
    return render_template('assign-supervisor.html')

@app.route("/postjob")
def postjob():
    return render_template('post-job.html')
