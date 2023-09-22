from flask import Flask, render_template, request, redirect, url_for
import pymysql 
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

# Configure your MySQL database connection
db_conn = pymysql.connect(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('company.html')

@app.route("/postjob", methods=['POST'])
def postjob():
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
        insert_sql = """
        INSERT INTO job_table (
            email, job_title, job_location, job_region, job_type, job_description,
            company_name, company_tagline, company_description, company_website,
            facebook_username, twitter_username, linkedin_username, featured_image_url, logo_url
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

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

# Define a route for the success page
@app.route("/success")
def success():
    return "Job data submitted successfully!"

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




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
