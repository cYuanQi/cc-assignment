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

@app.route("/postjob", methods=['GET','POST'])
def postjob():
    if request.method == 'POST':
        try:
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
            facebook_username = request.form['company_website_fb']
            twitter_username = request.form['company_website_tw']
            linkedin_username = request.form['company_website_li']

            # Get the uploaded files
            featured_image = request.files['featured_image']
            logo = request.files['logo']

            cursor = db_conn.cursor()

            # Insert job data into the job table
            insert_sql = "INSERT INTO job_table (email, job_title, job_location, job_region, job_type, job_description,company_name, company_tagline, company_description, company_website,facebook_username, twitter_username, linkedin_username, featured_image_url, logo_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            if featured_image.filename == "":
                cursor.close()
                return "Please select a featured image"

            if logo.filename == "":
                cursor.close()
                return "Please select a logo"

            try:
                # Upload featured image and logo to S3
                if featured_image.filename != "":
                    s3 = boto3.client('s3')
                    featured_image_name_in_s3 = "featured_" + featured_image.filename
                    s3.upload_fileobj(featured_image, custombucket, featured_image_name_in_s3)
                    featured_image_url = f"https://{custombucket}.s3.amazonaws.com/{featured_image_name_in_s3}"

                if logo.filename != "":
                    s3 = boto3.client('s3')
                    logo_image_name_in_s3 = "logo_" + logo.filename
                    s3.upload_fileobj(logo, custombucket, logo_image_name_in_s3)
                    logo_url = f"https://{custombucket}.s3.amazonaws.com/{logo_image_name_in_s3}"

                # After successfully storing in S3, store job details in the MySQL database
                cursor.execute(insert_sql, (
                    email, job_title, job_location, job_region, job_type, job_description,
                    company_name, company_tagline, company_description, company_website,
                    facebook_username, twitter_username, linkedin_username, featured_image_url, logo_url
                ))
                db_conn.commit()
            except Exception as e:
                cursor.close()
                return str(e)
            finally:
                cursor.close()

            return redirect(url_for('success'))  # Redirect to a success page or appropriate URL

        except Exception as e:
            return str(e)

    # If it's not a POST request, render the form
    return render_template('post-job.html')


# Define a route for the success page
@app.route("/success")
def success():
    return "Job data submitted successfully!"


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
