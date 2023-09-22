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

# Allowed file extensions for resume uploads
ALLOWED_EXTENSIONS = {'jpg'}

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route("/")
def home():
    return render_template('admin.html')

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')

@app.route("/AddAdmin", methods=['GET', 'POST'])
def AddAdmin():
    return render_template('addadmin.html')

@app.route("/addAdminProcess", methods=['POST'])
def addAdminProcess():
    adm_id = request.form['adm_id']
    adm_name = request.form['adm_name']
    adm_gender = request.form['adm_gender']
    adm_dob = request.form['adm_dob']
    adm_address = request.form['adm_address']
    adm_email = request.form['adm_email']
    adm_phone = request.form['adm_phone']
    adm_img = request.files['adm_img']

    cursor = db_conn.cursor()
    insert_sql = "INSERT INTO adm_profile(adm_id, adm_name, adm_gender, adm_dob, adm_address, adm_email, adm_phone, adm_img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    if adm_img == "":
        return "Please select an image"

    try:
        cursor.execute(insert_sql, (adm_id, adm_name, adm_gender, adm_dob, adm_address, adm_email, adm_phone, ""))
        db_conn.commit()

        # Upload image file to S3
        adm_file_name_in_s3 = "adm-id-" + str(adm_id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=adm_file_name_in_s3, Body=adm_img)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                adm_file_name_in_s3)

            # Update the image file name in the database
            update_sql = "UPDATE adm_profile SET adm_img = %s WHERE adm_id = %s"
            cursor.execute(update_sql, (adm_file_name_in_s3, adm_id))
            db_conn.commit()

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    return render_template('admin_list.html')

    
@app.route("/admin_list")
def admin_list():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM adm_profile')
    rows = cursor.fetchall()
    cursor.close()
    return render_template('admin_list.html', rows=rows)


@app.route("/companylistadm", methods=['GET', 'POST'])
def companylistadm():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM testing_company')
    rows = cursor.fetchall()
    cursor.close()
    return render_template('company_list_adm.html', rows=rows)

import random
import string

def generate_company_id(length=8):
    # Generate a random string of uppercase letters and digits
    company_id = 'C' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length - 1))

    return company_id


@app.route("/approve_or_reject_company", methods=['POST'])
def approve_or_reject_company():
    comp_name = request.form['company_name']
    action = request.form['action']  # 'approve' or 'reject'

    cursor = db_conn.cursor()

    # Generate a unique company ID
    company_id = generate_company_id()

    # Retrieve the comp_id and comp_background from testing_company
    cursor.execute("SELECT comp_name, comp_background FROM testing_company WHERE comp_name = %s", (comp_name,))
    company_info = cursor.fetchone()  # Assuming only one row matches

    if company_info:
        comp_name, comp_background = company_info
    else:
        # Handle the case where company_info is not found
        comp_name = None
        comp_background = None

    # Insert the approval/rejection record into the history table with the generated company ID
    insert_sql = "INSERT INTO company_approval_history (company_name, approval_status, timestamp, comp_background) VALUES (%s, %s, NOW(), %s)"
    cursor.execute(insert_sql, (comp_name, action.capitalize(), comp_background))
    db_conn.commit()

    # Delete the company information from testing_company
    delete_sql = "DELETE FROM testing_company WHERE comp_name = %s"
    cursor.execute(delete_sql, (comp_name,))
    db_conn.commit()

    cursor.close()

    return render_template('company_list_or_history.html')  # Replace with the actual URL

@app.route("/assignsupervisor", methods=['GET', 'POST'])
def assignsupervisor():
    return render_template('assign-supervisor.html')

@app.route("/nologin", methods = ['GET', 'POST'])
def nologin():
    return render_template('no_login.html')

@app.route("/jobsingle", methods = ['GET', 'POST'])
def jobsingle():
    return render_template('job-single.html')

@app.route("/assignsupervisorProcess", methods=['GET','POST'])
def assignsupervisorProcess():
    stud_name = request.form['stud_name']
    stud_id = request.form['stud_id']
    sup_name = request.form['sup_name']
    sup_id = request.form['sup_id']

    cursor = db_conn.cursor()
    insert_sql = "INSERT INTO admin(stud_name, stud_id, sup_name, sup_id) VALUES (%s, %s, %s, %s)"
    

    cursor.execute(insert_sql, (stud_name, stud_id, sup_name, sup_id))
    db_conn.commit()

    cursor.close()

    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM admin')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('assign-supervisor-Output.html', rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
