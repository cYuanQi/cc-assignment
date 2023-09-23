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
    return render_template('company.html')

@app.route("/company", methods=['GET', 'POST'])
def company():
    return render_template('company.html')

@app.route("/postjob", methods=['GET', 'POST'])
def postjob():
    if request.method == 'POST': 
 
            # Get data from the form
            email = request.form['email']
            job_title = request.form['job_title']
            job_location = request.form['job_location']
            job_region = request.form['job_region']
            job_type = request.form['job_type']
            job_description = request.form['job_description']
            company_name = request.form['company_name']
            company_tagline = request.form['company_tagline']
            company_description = request.form['company_description']
            company_website = request.form['company_website']
            facebook_username = request.form['twitter_username']
            twitter_username = request.form['twitter_username']
            linkedin_username = request.form['linkedin_username']

            # Get the uploaded files
            logo = request.files['logo']

            cursor = db_conn.cursor()

            # Insert job data into the job table
            insert_sql = "INSERT INTO job_table (email, job_title, job_location, job_region, job_type, job_description, company_name, company_tagline, company_description, company_website, facebook_username, twitter_username, linkedin_username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"

            cursor.execute(insert_sql, (email, job_title, job_location, job_region, job_type,  job_description, company_name, company_tagline, company_description,  company_website, facebook_username, twitter_username, linkedin_username))
          
            db_conn.commit()
            return render_template('success.html')
         
    # If it's not a POST request, render the form
    #return render_template('post-job.html')
    return redirect(url_for('postjob1', message='Student have successfully approve'))

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

 
    return redirect(url_for('approve_student1', message='Student have successfully approve'))


@app.route("/CompanyConfStudApp")
def  postjob1():
    # Retrieve the message query parameter from the URL
    message = request.args.get('message')

    #Render the job-single.html template with the message
    return render_template('CompanyConfStudApp.html', message=message)


@app.route("/post-job")
def  approve_student1():
    # Retrieve the message query parameter from the URL
    message = request.args.get('message')

    #Render the job-single.html template with the message
    return render_template('CompanyConfStudApp.html', message=message)



@app.route("/CompanyConfStudApp", methods=['GET', 'POST'])
def CompanyConfStudApp():
    return render_template('CompanyConfStudApp.html')

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
