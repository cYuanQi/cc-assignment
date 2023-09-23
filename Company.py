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
output = {}
table = 'job_table'


ALLOWED_EXTENSIONS = {'pdf'}

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('company.html')

@app.route("/company", methods=['GET', 'POST'])
def company():
    return render_template('company.html')

@app.route("/postjob", methods=['GET', 'POST'])
def postjob():
    message = request.args.get('message')
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
        featured_image = request.files['featured_image']
        logo = request.files['logo']

        cursor = db_conn.cursor()

        # Insert job data into the job table
        insert_sql = "INSERT INTO job_table (email, job_title, job_location, job_region, job_type, job_description, company_name, company_tagline, company_description, company_website, facebook_username, twitter_username, linkedin_username) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, )"
        cursor.execute(insert_sql, (email, job_title, job_location, job_region, job_type,  job_description, company_name, company_tagline, company_description,  company_website, facebook_username, twitter_username, linkedin_username ))
        if featured_image.filename == "":
            cursor.close()  # Close the cursor before returning
            return "Please select a file"

        if logo.filename == "":
            cursor.close()  # Close the cursor before returning
            return "Please select a file"
           
        try:
            # Upload resume file to S3
            featured_image_file_name_in_s3 = str(company_name) + "_image_file"
            logo_file_name_in_s3 = str(company_name) + "_logo"
            s3 = boto3.resource('s3')
            
            try:
                print("Data inserted in MySQL RDS... uploading image to S3...")
                s3.Bucket(custombucket).put_object(Key=featured_image_file_name_in_s3, Body=featured_image)
                s3.Bucket(custombucket).put_object(Key=logo_file_name_in_s3, Body=logo)
                bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
                s3_location = (bucket_location['LocationConstraint'])

                if s3_location is None:
                    s3_location = ''
                else:
                    s3_location = '-' + s3_location


                object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                    s3_location,
                    custombucket,
                    featured_image_file_name_in_s3)           

                object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                    s3_location,
                    custombucket,
                    logo_file_name_in_s3)

            except Exception as e:
                cursor.close()  # Close the cursor before returning
                return str(e)
            
            cursor.execute(insert_sql, (email, job_title, job_location, job_region, job_type,  job_description, company_name, company_tagline, company_description,  company_website, facebook_username, twitter_username, linkedin_username ))
            db_conn.commit()
        finally:
            cursor.close()  # Close the cursor in the finally block

            

        flash("Job posted successfully!", "success")
        return redirect(url_for('postjob', message='success'))

    # If it's not a POST request, render the form
    return render_template('post-job.html')


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





# Define a route for the success page
@app.route("/success")
def success():
    return "Job data submitted successfully!"


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
