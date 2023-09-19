from flask import Flask, render_template, request
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
# 

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('login.html')

# USer Sign up - stud, lecturer
@app.route("/adduser", methods=['POST'])
def AddUser():
    user_name = request.form['user_name']
    user_email = request.form['user_email']
    user_password = request.form['user_password']
    user_repassword = request.form['user_repassword']

    # Check the email domain to determine the role and redirect accordingly
    if user_email.endswith('@company.com'):
        return "Please sign up in another form!"
    else: 
        if user_email.endswith('@student.com'):
            user_role = "student"
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


# Register Company
@app.route("/addCompany", methods=['POST'])
def AddCompany():
    company_name = request.form['company_name']
    company_email = request.form['company_email']
    company_password = request.form['company_password']
    company_repassword = request.form['company_repassword']
    user_role = "lecturer"

    cursor.execute(insert_sql, (user_role, company_name, company_email, company_password))
    cursor = db_conn.cursor()

    if user_password != user_repassword:
        return "Please check your password!"

    try:
        cursor.execute(insert_sql, (company_name, company_email, company_password))
        db_conn.commit()

    except Exception as e:
        return str(e)
    finally:
        cursor.close()

    print("all modification done...")
    return render_template('login.html', show_msg="Your registration was successful. Please wait for admin approval.")


# Login
@app.route("/userlogin", methods=['POST'])
def UserLogin():
    user_email = request.form['user_email']
    user_password = request.form['user_password']

    cursor.execute("SELECT * FROM login WHERE email=%s", (user_email,))
    user = cursor.fetchone()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)