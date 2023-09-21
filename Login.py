from flask import Flask, render_template, request, session
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

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

    session['email'] = user_email

    # Check the email domain to determine the role and redirect accordingly
    if user_email.endswith('@student.com'):
        user_role = "student"
    elif user_email.endswith('@company.com'):
        user_role = "company"
    elif user_email.endswith('@admin.com'):
        user_role = "admin"
    elif user_email.endswith('@lecturer.com'):
        user_role = "lecturer"

    insert_sql = "INSERT INTO login VALUES (%s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if user_password != user_repassword:
        return "Please check your password!"

    try:
        cursor.execute(insert_sql, (user_role, user_name, user_email, user_password))
        db_conn.commit()

    except Exception as e:
        return str(e)
    finally:
        cursor.close()

    print("all modification done...")
    return render_template('login.html', show_msg="Signup successful!")

# Login
@app.route("/userlogin", methods=['POST'])
def UserLogin():
    user_email = request.form['loginEmail']
    user_password = request.form['loginPassword']

    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM login WHERE user_email=%s", (user_email,))
    user = cursor.fetchall()
    cursor.close()

    if user:
        # Check the email domain to determine the role and redirect accordingly
        if user_email.endswith('@student.com'):
            return render_template('user_page.html')
        elif user_email.endswith('@admin.com'):
            return render_template('admin.html')
        elif user_email.endswith('@lecturer.com'):
            return render_template('lecture.html')
        elif user_email.endswith('@company.com'):
            return render_template('company.html')
    else:
        return render_template('login.html', show_msg="User does not exist")

# --------------------Lecture to Lecturer details--------------------

@app.route("/lecturerdetails", methods=['GET', 'POST'])
def lecturerdetails():
    email = session.get('email')
    return render_template('lecturer-details.html')

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

@app.route("/lecture", methods=['GET', 'POST'])
def lecture():
    return render_template('lecture.html')

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
