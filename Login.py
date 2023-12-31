from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
# , session
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)
app.secret_key = 'de3bff82a9f94e920d78e0c42311dd68'

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)
output = {}
table = 'login'

# -----------------------------------------------------------------

# How to keep email that user used to login
@app.route("/", methods=['GET', 'POST'])
def home():
    # return render_template('login.html')
    return render_template('login.html')

# --------------------Login.html to own hoempage--------------------
# User Sign up
@app.route("/adduser", methods=['POST'])
def AddUser():
    user_name = request.form['name']
    user_email = request.form['email']
    user_password = request.form['password']
    user_repassword = request.form['retypePassword']

    #RuntimeError
    #RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.
    # session['email'] = user_email

    # Check the email domain to determine the role and redirect accordingly
    if user_email.endswith('@student.com'):
        user_role = "student"
    elif user_email.endswith('@company.com'):
        user_role = "company"
    elif user_email.endswith('@admin.com'):
        user_role = "admin"
    elif user_email.endswith('@lecturer.com'):
        user_role = "lecturer"
        insert_lec_sql = "INSERT INTO lecturer_details VALUE (%s, %s, '', '', '')"
    else:
        # return render_template('login.html', show_msg="User does not exist")
        return render_template('login.html', show_msg="Email format invalid!")

    insert_sql = "INSERT INTO login VALUES (%s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if user_password != user_repassword:
        return render_template('login.html', show_msg="Please check your password!")

    try:
        cursor.execute(insert_sql, (user_name, user_email, user_password, user_role))
        if user_role == "lecturer":
            cursor.execute(insert_lec_sql, (user_name, user_email))
        db_conn.commit()

    except Exception as e:
        return str(e)
    finally:
        cursor.close()

    #print("all modification done...")
    return render_template('login.html', show_msg="Sign Up successful! You can login now!~")

# Login
@app.route("/userlogin", methods=['POST'])
def UserLogin():
    user_email = request.form['loginEmail']
    user_password = request.form['loginPassword']

    # cursor = db_conn.cursor()
    # cursor.execute("SELECT * FROM login WHERE user_email=%s", (user_email,))
    # user = cursor.fetchall()
    # cursor.close()

    # if user:
    if user_email:
        # Check the email domain to determine the role and redirect accordingly
        if user_email.endswith('@student.com'):
            return redirect(url_for('userpage', user_email=user_email))
        elif user_email.endswith('@admin.com'):
            return redirect(url_for('admin', user_email=user_email))
        elif user_email.endswith('@lecturer.com'):
            return redirect(url_for('lecturer', user_email=user_email))
        elif user_email.endswith('@company.com'):
            return redirect(url_for('company', user_email=user_email))
    else:
        # return render_template('login.html', show_msg="User does not exist")
        return render_template('login.html', show_msg="Email format invalid!")

# --------------------Lecture to Lecturer details--------------------

@app.route("/submitlecdetails/<user_email>", methods=['GET', 'POST'])
def submitlecdetails(user_email):

    # email = session.get('email')

    select_sql = "SELECT * FROM lecturer_details WHERE lecturer_email = %s"
    cursor = db_conn.cursor()
    cursor.execute(select_sql, (user_email,))
    lecturer = cursor.fetchone()
    
    # details of form
    lecturer_name = request.form['lecturerName']
    lecturer_faculty = request.form['lecturerFaculty']
    lecturer_department = request.form['lecturerDepartement']
    lecturer_position = request.form['lecturerPosition']

    if not lecturer:
        insert_sql = "INSERT INTO lecturer_details VALUES (%s, %s, %s, %s, %s)"

        try:
            cursor.execute(insert_sql, (lecturer_name, user_email, lecturer_faculty, lecturer_department, lecturer_position))
            db_conn.commit()
        
        except Exception as e:
            return str(e)
        finally:
            cursor.close()
    else:
        update_sql = "UPDATE lecturer_details SET lecturer_name = %s, lecturer_faculty = %s, lecturer_department = %s, lecturer_position = %s WHERE lecturer_email = %s"
        
        try:
            cursor.execute(update_sql, (lecturer_name, lecturer_faculty, lecturer_department, lecturer_position, user_email))
            db_conn.commit()
        except Exception as e:
            return str(e)
        finally:
            cursor.close()
    
    return redirect(url_for('lecturerdetails', user_email=user_email))

# --------------------GENERAL redirect--------------------

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

@app.route("/lecturer/<user_email>", methods=['GET', 'POST'])
def lecturer(user_email):
    return render_template('lecture.html', user_email=user_email)

@app.route("/lecturerdetails/<user_email>", methods=['GET', 'POST'])
def lecturerdetails(user_email):
    # Fetch the lecturer details based on the user_email
    select_sql = "SELECT * FROM lecturer_details WHERE lecturer_email = %s"
    cursor = db_conn.cursor()
    cursor.execute(select_sql, (user_email,))
    lecturer = cursor.fetchone()
    
    # Initialize lecturer as an empty dictionary if it's None
    lecturer = lecturer or {}

    # Fetch the user details based on the user_email
    select_user_sql = "SELECT user_name, user_email FROM login WHERE user_email = %s"
    cursor.execute(select_user_sql, (user_email,))
    user = cursor.fetchone()

    cursor.close()

    # Determine which data to pass based on whether lecturer exists
    if lecturer == {}:
        return render_template('lecturer-details.html', data=user)  # Pass 'user' data
    else:
        return render_template('lecturer-details.html', data=lecturer)  # Pass 'lecturer' data

# @app.route("/evaluatereport", methods=['GET', 'POST'])
# def evaluatereport():
#     return render_template('EvaluateReport.html')

# @app.route("/gradereport", methods=['GET', 'POST'])
# def gradereport():
#     return render_template('Grade.html')

@app.route("/company/<user_email>", methods=['GET', 'POST'])
def company(user_email):
    return render_template('company1.html', user_email=user_email)

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
    
@app.route("/userpage/<user_email>", methods=['GET', 'POST'])
def userpage(user_email):
    return render_template('user_page1.html', user_email=user_email)
    
@app.route("/admin/<user_email>", methods=['GET', 'POST'])
def admin(user_email):
    return render_template('admin1.html', user_email=user_email)

@app.route("/AddAdmin", methods=['GET', 'POST'])
def AddAdmin():
    return render_template('addadmin.html')

@app.route("/CompanyConfStudApp", methods=['GET', 'POST'])
def CompanyConfStudApp():
    return render_template('CompanyConfStudApp.html')

@app.route("/portfolio_single_yq", methods=['GET', 'POST'])
def portfolio_single_yq():
    return render_template('portfolio-single-yq.html')

@app.route("/portfoliosinglejd", methods=['GET', 'POST'])
def portfoliosinglejd():
    return render_template('portfolio-single-jd.html')

@app.route("/portfoliosinglebx", methods=['GET', 'POST'])
def portfoliosinglebx():
    return render_template('portfolio-single-bx.html')

@app.route("/portfolio_single_janet", methods=['GET', 'POST'])
def portfolio_single_janet():
    return render_template('portfolio-single-Janet.html')

@app.route("/portfolio_single_ken", methods=['GET', 'POST'])
def portfolio_single_ken():
    return render_template('portfolio-single-ken.html')
    
@app.route("/portfolio_single_duwee", methods=['GET', 'POST'])
def portfolio_single_duwee():
    return render_template('portfolio-single-duwee.html')

# -----------------------BO XIN------------------------------------

table = 'lecturer'

# Allowed file extensions for resume uploads
ALLOWED_EXTENSIONS = {'pdf'}

@app.route("/evaluatereport/<user_email>", methods=['GET', 'POST'])
def evaluatereport(user_email):
    cursor = db_conn.cursor()

    try:
        if request.method == 'GET':
            # Execute a SELECT query to fetch the reports
            select_sql = "SELECT * FROM report WHERE sup_email = %s"
            cursor.execute(select_sql, (user_email,))
            reports = cursor.fetchall()

            return render_template('EvaluateReport.html', reports=reports)

    finally:
        cursor.close()

@app.route("/downloadreport/<report_name>", methods=['GET'])
def downloadreport(report_name):
    try:
        # Specify the S3 bucket name
        s3_bucket_name = custombucket

        # Create a new S3 client
        s3 = boto3.client('s3')

        # Generate a pre-signed URL for the S3 object
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': s3_bucket_name, 'Key': report_name},
            ExpiresIn=3600  # URL expiration time in seconds (adjust as needed)
        )

        # Create a response with the pre-signed URL for the download
        return redirect(url)

    except Exception as e:
        return str(e)


@app.route("/gradereport/<user_email>", methods=['GET', 'POST'])
def gradereport(user_email):
    cursor = db_conn.cursor()

    try:
        if request.method == 'GET':
            # Execute a SELECT query to fetch the reports
            select_sql = "SELECT * FROM report WHERE sup_email = %s"
            cursor.execute(select_sql, (user_email,))
            reports = cursor.fetchall()

            return render_template('Grade.html', reports=reports)

    finally:
        cursor.close()
        

@app.route("/updatescore/<report_name>", methods=['POST', 'GET'])
def updatescore(report_name):
    cursor = db_conn.cursor()
    try:
        # Check if a grade is selected in the URL query parameters
        student_score = request.args.get('grade')

        if student_score is not None:
            # Update the student_score for the specified report_name
            update_sql = "UPDATE report SET student_score = %s WHERE report_name = %s"
            cursor.execute(update_sql, (student_score, report_name))
            db_conn.commit()

            flash("Report graded and data updated in the database.", "success")
        else:
            flash("Please select a grade to update the score.", "error")

        return str("Sucessfully updated the student score.")
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
