# Import additional modules
from flask import Flask, render_template, request, redirect, url_for, flash
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
        facebook_username = request.form['company_website_fb']
        twitter_username = request.form['company_website_tw']
        linkedin_username = request.form['company_website_li']

        # Get the uploaded files
        featured_image = request.files['featured_image']
        logo = request.files['logo']

        # Check if required fields are not empty
        if not email or not job_title or not company_name:
            flash('Please fill out all required fields.', 'error')
        else:
            try:
                cursor = db_conn.cursor()

                # Insert job data into the job table
                insert_sql = """
                INSERT INTO job_table (
                    email, job_title, job_location, job_region, job_type, job_description,
                    company_name, company_tagline, company_description, company_website,
                    facebook_username, twitter_username, linkedin_username, featured_image_url, logo_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                if featured_image and featured_image.filename != "":
                    # Upload featured image to S3
                    s3 = boto3.client('s3')
                    featured_image_name_in_s3 = "featured_" + featured_image.filename
                    s3.upload_fileobj(featured_image, custombucket, featured_image_name_in_s3)
                    featured_image_url = f"https://{custombucket}.s3.amazonaws.com/{featured_image_name_in_s3}"
                else:
                    featured_image_url = None

                if logo and logo.filename != "":
                    # Upload logo to S3
                    s3 = boto3.client('s3')
                    logo_image_name_in_s3 = "logo_" + logo.filename
                    s3.upload_fileobj(logo, custombucket, logo_image_name_in_s3)
                    logo_url = f"https://{custombucket}.s3.amazonaws.com/{logo_image_name_in_s3}"
                else:
                    logo_url = None

                # After successfully storing in S3, store job details in the MySQL database
                cursor.execute(insert_sql, (
                    email, job_title, job_location, job_region, job_type, job_description,
                    company_name, company_tagline, company_description, company_website,
                    facebook_username, twitter_username, linkedin_username, featured_image_url, logo_url
                ))
                db_conn.commit()
                cursor.close()

                flash('Job data submitted successfully!', 'success')
                return redirect(url_for('success'))  # Redirect to a success page or appropriate URL
            except Exception as e:
                flash(str(e), 'error')
                return redirect(url_for('home'))

    return render_template('post-job.html')

@app.route("/success")
def success():
    return "Job data submitted successfully!"

# ... Define other routes and functions as needed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
