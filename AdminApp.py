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

@app.route("/")
def home():
    return render_template('admin.html')

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')

@app.route("/AddAdmin", methods=['GET', 'POST'])
def AddAdmin():
    return render_template('addadmin.html')

@app.route("/addAdminProcess", methods=['GET', 'POST'])
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
    insert_sql = "INSERT INTO adm_profile(adm_id, adm_name, adm_gender, adm_dob, adm_address, adm_email, adm_phone) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    if adm_img == "":
        return "Please select an image"

    try:
        cursor.execute(insert_sql, (adm_id, adm_name, adm_gender, adm_dob, adm_address, adm_email, adm_phone))
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

            # Save the image file name in the database
            update_sql = "UPDATE adm_profile SET adm_image = %s WHERE adm_id = %s"
            cursor.execute(update_sql, (adm_file_name_in_s3, adm_id))
            db_conn.commit()

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    return render_template('admin_list.html', rows=rows)

@app.route("/adminProfile/<email>", methods=['GET'])
def adminProfile(email):
    cursor = db_conn.cursor()
    select_sql = "SELECT * FROM adm_profile WHERE adm_email = %s"

    try:
        cursor.execute(select_sql, (email,))
        adminData = cursor.fetchone()

        if adminData:
            adm_image_file_name = adminData[8]  # Assuming the image file name is in the 8th column
        else:
            return "Administrator not found"  # Handle case when administrator is not found

    except Exception as e:
        return str(e)
    finally:
        cursor.close()

    return render_template('admin_profile.html', adminData=adminData, adm_image_file_name=adm_image_file_name)

    
@app.route("/companylistadm", methods=['GET', 'POST'])
def companylistadm():
    return render_template('company_list_adm.html')


@app.route("/assignsupervisor", methods=['GET', 'POST'])
def assignsupervisor():
    return render_template('assign-supervisor.html')

@app.route("/nologin", methods = ['GET', 'POST'])
def nologin():
    return render_template('no_login.html')

@app.route("/jobsingle", methods = ['GET', 'POST'])
def jobsingle():
    return render_template('job-single.html')

@app.route("/assignsupervisorProcess", methods=['POST'])
def assignsupervisorProcess():
    stud_name = request.form['stud_name']
    stud_id = request.form['stud_id']
    sup_name = request.form['sup_name']
    sup_id = request.form['sup_id']

    
    insert_sql = "INSERT INTO admin VALUES (%s, %s, %s, %s)"
    cursor = db_conn.cursor()

    cursor.execute(insert_sql, (stud_name, stud_id, sup_name, sup_id))
    db_conn.commit()
    cursor.close()

    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM admin')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('assign-supervisor-Output.html', name=adm_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
