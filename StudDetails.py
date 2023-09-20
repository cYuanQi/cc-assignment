# Import additional modules
from flask import Flask, render_template, request, redirect, url_for, flash
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)
app.secret_key = 'de3bff82a9f94e920d78e0c42311dd68' 

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
        student_name = request.form['studentName']
        student_email = request.form['studentEmail']
        student_programme = request.form['studentProgramme']
        student_skills = request.form['studentSkills']
        resume_file = request.files['studentResume']

        # Ensure that the 'uploads' directory exists
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        # Check if a file is selected and has the allowed extension
        if resume_file and allowed_file(resume_file.filename):
            # Upload resume file to the 'uploads' directory
            resume_filename = os.path.join('uploads', resume_file.filename)
            resume_file.save(resume_filename)
        else:
            flash('Invalid resume file. Please upload a PDF file.', 'error')
            return redirect(url_for('student_details_form'))

        # Insert student data into the database
        cursor = db_conn.cursor()
        insert_sql = "INSERT INTO student_detail (student_name, student_email, student_programme, student_skills, resume_file) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_sql, (student_name, student_email, student_programme, student_skills, resume_filename))
        db_conn.commit()
        cursor.close()

        flash('Student data saved successfully', 'success')

        # Redirect to the route that displays the inserted data
        return redirect(url_for('display_student_data', user_email=student_email))

# Route to display the inserted student data
@app.route("/view_student/<user_email>", methods=['GET'])
def display_student_data(user_email):
    cursor = db_conn.cursor()
    select_sql = "SELECT * FROM student_detail WHERE student_email = %s"
    cursor.execute(select_sql, (user_email,))
    student_data = cursor.fetchone()
    cursor.close()

    return render_template('display_student_data.html', student_data=student_data)

# Route to download the student's resume
@app.route("/download_resume/<filename>", methods=['GET'])
def download_resume(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/nologin", methods=['GET', 'POST'])
def nologin():
    return render_template('no_login.html')
    
@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route("/joblistings", methods=['GET', 'POST'])
def joblistings():
    return render_template('job-listings.html')

@app.route("/jobsingle", methods=['GET', 'POST'])
def jobsingle():
    return render_template('job-single.html')

@app.route("/services", methods=['GET', 'POST'])
def services():
    return render_template('services.html')

@app.route("/servicesingle", methods=['GET', 'POST'])
def servicesingle():
    return render_template('service-single.html')

@app.route("/blog", methods=['GET', 'POST'])
def blog():
    return render_template('blog.html')

@app.route("/blogsingle", methods=['GET', 'POST'])
def blogsingle():
    return render_template('blog-single.html')

@app.route("/portfolio", methods=['GET', 'POST'])
def portfolio():
    return render_template('portfolio.html')

@app.route("/portfoliosingle", methods=['GET', 'POST'])
def portfoliosingle():
    return render_template('portfolio-single.html')

@app.route("/testimonials", methods=['GET', 'POST'])
def testimonials():
    return render_template('testimonials.html')

@app.route("/faq", methods=['GET', 'POST'])
def faq():
    return render_template('faq.html')

@app.route("/gallery", methods=['GET', 'POST'])
def gallery():
    return render_template('gallery.html')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route("/lecture", methods=['GET', 'POST'])
def lecture():
    return render_template('lecture.html')

@app.route("/lecturerdetails", methods=['GET', 'POST'])
def lecturerdetails():
    return render_template('lecturer-details.html')

@app.route("/evaluatereport", methods=['GET', 'POST'])
def evaluatereport():
    return render_template('EvaluateReport.html')

@app.route("/grade", methods=['GET', 'POST'])
def grade():
    return render_template('Grade.html')

@app.route("/company", methods=['GET', 'POST'])
def company():
    return render_template('company.html')

@app.route("/postjob", methods=['GET', 'POST'])
def postjob():
    return render_template('post-job.html')

@app.route("/studentapplyjobs", methods=['GET', 'POST'])
def studentapplyjobs():
    return render_template('StudentApplyJobs.html')

@app.route("/companylistadm", methods=['GET', 'POST'])
def companylistadm():
    return render_template('company_list_adm.html')

@app.route("/assignsupervisor", methods=['GET', 'POST'])
def assignsupervisor():
    return render_template('assign-supervisor')

@app.route("/studentreport", methods=['GET', 'POST'])
def studentreport():
    return render_template('Student_report.html')

@app.route("/studentdetails", methods=['GET', 'POST'])
def studentdetails():
    return render_template('student-details.html')

@app.route("/userpage", methods=['GET', 'POST'])
def userpage():
    return render_template('user_page.html')

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
