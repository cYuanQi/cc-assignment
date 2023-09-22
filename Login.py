from flask import Flask, render_template, request, redirect, url_for
# , session
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

    # cursor = db_conn.cursor()
    # cursor.execute("SELECT * FROM login WHERE user_email=%s", (user_email,))
    # user = cursor.fetchall()
    # cursor.close()

    # if user:
    if user_email:
        # Check the email domain to determine the role and redirect accordingly
        if user_email.endswith('@student.com'):
            return render_template('user_page.html', user_email=user_email)
        elif user_email.endswith('@admin.com'):
            return render_template('admin.html', user_email=user_email)
        elif user_email.endswith('@lecturer.com'):
            return redirect(url_for('lecturer', user_email=user_email))
        elif user_email.endswith('@company.com'):
            return render_template('company.html', user_email=user_email)
    else:
        # return render_template('login.html', show_msg="User does not exist")
        return render_template('login.html', show_msg="Email format invalid!")

# --------------------Lecture to Lecturer details--------------------

@app.route("/submitlecdetails/<user_email>", methods=['GET', 'POST'])
def submitlecdetails(user_email):

    # email = session.get('email')

    select_sql = "SELECT * FROM lecturer WHERE lecturer_email = %s"
    cursor = db_conn.cursor()
    cursor.execute(select_sql, (user_email,))
    lecturer = cursor.fetchone()
    
    # details of form
    lecturer_name = request.form['lecturerName']
    lecturer_email = request.form['lecturerEmail']
    lecturer_faculty = request.form['lecturerFaculty']
    lecturer_department = request.form['lecturerDepartement']
    lecturer_position = request.form['lecturerPosition']

    if not lecturer:
        insert_sql = "INSERT INTO lecturer VALUES (%s, %s, %s, %s, %s)"

        try:
            cursor.execute(insert_sql, (lecturer_name, lecturer_email, lecturer_faculty, lecturer_department, lecturer_position))
            db_conn.commit()
        
        except Exception as e:
            return str(e)
        finally:
            cursor.close()
    else:
        update_sql = "UPDATE lecturer SET lecturer_name = %s, lecturer_faculty = %s, lecturer_department = %s, lecturer_position = %s WHERE lecturer_email = %s"
        
        try:
            cursor.execute(update_sql, (lecturer_name, lecturer_faculty, lecturer_department, lecturer_position, lecturer_email))
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

# @app.route("/lecturerdetails/<user_email>", methods=['GET', 'POST'])
# def lecturerdetails(user_email):
#     # email = session.get('email')

#     select_sql = "SELECT * FROM lecturer_details WHERE lecturer_email = %s"
#     cursor = db_conn.cursor()
#     cursor.execute(select_sql, (user_email,))
#     lecturer = cursor.fetchone()
    
#     # Initialize lecturer as an empty dictionary if it's None
#     lecturer = lecturer or {}
    
#     if lecturer:
#         cursor.close()
        
#         return render_template('lecturer-details.html', lecturer = lecturer)
#     else:
#         select_sql = "SELECT * FROM login WHERE user_email = %s"
#         cursor.execute(select_sql, (user_email,))
#         user = cursor.fetchone()
#         cursor.close()

#         return render_template('lecturer-details.html', user = user)

@app.route("/lecturerdetails/<user_email>", methods=['GET', 'POST'])
def lecturerdetails(user_email):
    # email = session.get('email')

    select_sql = "SELECT * FROM lecturer_details WHERE lecturer_email = %s"
    cursor = db_conn.cursor()
    cursor.execute(select_sql, (user_email,))
    lecturer = cursor.fetchone()

    # Initialize lecturer as an empty dictionary if it's None
    lecturer = lecturer or {}

    select_sql = "SELECT * FROM login WHERE user_email = %s"
    cursor.execute(select_sql, (user_email,))
    user = cursor.fetchone()

    cursor.close()

    # Determine which data to pass based on whether lecturer exists
    if lecturer:
        return render_template('lecturer-details.html', data=lecturer)
    else:
        return render_template('lecturer-details.html', data=user)

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
