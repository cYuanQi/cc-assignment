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
table = 'lecturer'

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('lecture.html')

# Allowed file extensions for resume uploads
ALLOWED_EXTENSIONS = {'pdf'}

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/EvaluateReport/<user_email>", methods=['GET'])
def evaluate_report(user_email):
    cursor = db_conn.cursor()
    select_sql = "SELECT * FROM report WHERE sup_email = %s"
    cursor.execute(select_sql, (user_email,))
    report_data = cursor.fetchone()
    cursor.close()
        
    if report_data:
        # Assuming student_data[4] contains the resume file name in S3
        report_name = report_data[0]
        student_name = report_data[1]

        # Retrieve the resume file from S3
        s3 = boto3.client('s3')
        try:
            s3_object = s3.get_object(Bucket=custombucket, Key=report_name)
            report_file_data = s3_object['Body'].read()
        except Exception as e:
            return str(e)  # Handle S3 retrieval error

        # You can now pass the resume_data to your template for download
        return render_template('EvaluateReport.html', report_data=report_data, report_name=report_name, student_name=student_name)
    else:
        return "Report not found"  # Handle student not found error

def fetchreports():
    cursor = db_conn.cursor()
    try:
        # Execute a SELECT query to fetch the reports
        select_sql = "SELECT * FROM report WHERE sup_email = %s"
        cursor.execute(select_sql)
        reports = cursor.fetchall()
        cursor.close()
        return reports
    except Exception as e:
        cursor.close()
        print(f"Error fetching reports: {e}")
        return []  # Return an empty list in case of an error


@app.route("/download_report/<report_name>", methods=['GET'])
def downloadreport(report_name):
    # Specify the S3 bucket name
    s3_bucket_name = custombucket

    # Create a new S3 client
    s3 = boto3.client('s3')

    try:
        # Generate a pre-signed URL for the S3 object
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': s3_bucket_name, 'Key': report_name},
            ExpiresIn=3600  # URL expiration time in seconds (adjust as needed)
        )

        # Redirect the user to the pre-signed URL, which will trigger the file download
        return redirect(url)
    except Exception as e:
        return str(e)


def gradereport():
    if request.method == 'POST':
        reports = fetchreports()  # Implement this function to fetch reports

         # Check if any reports were found
        if not reports:
            return "No reports found to grade."

        for report in reports:
            report_name = report[0]  # Assuming the report_id is in the first column of your report table
            student_score = request.form.get(f'student_score_{report_name}')

            if student_score is not None:
                cursor = db_conn.cursor()
                try:
                    # Update the student_score for the specified report_id
                    update_sql = "UPDATE report SET student_score = %s WHERE report_name = %s"
                    cursor.execute(update_sql, (student_score, report_name))
                    db_conn.commit()
                    cursor.close()
                except Exception as e:
                    cursor.close()
                    print(f"Error updating student_score: {e}")
                    return "An error occurred while updating the student_score."

        flash("Reports graded and data updated in the database.", "success")
        return redirect(url_for('grade'))

    reports = fetch_reports()
    return render_template('Grade.html', reports=reports)



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

@app.route("/lecture")
def lecturer():
    return render_template('lecture.html')

@app.route("/lecturerdetails")
def lecturerdetails():
    return render_template('lecturer-details.html')

@app.route("/evaluatereport")
def evaluatereport():
    return render_template('EvaluateReport.html')

@app.route("/grade")
def grade():
    return render_template('Grade.html')

@app.route("/company")
def company():
    return render_template('company.html')

@app.route("/postjob")
def postjob():
    return render_template('post-job.html')

@app.route("/studentapplyjobs")
def studentapplyjobs():
    return render_template('StudentApplyJobs.html')

@app.route("/companylistadm")
def companylistadm():
    return render_template('company_list_adm.html')

@app.route("/assignsupervisor")
def assignsupervisor():
    return render_template('assign-supervisor.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
