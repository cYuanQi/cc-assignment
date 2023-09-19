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
table = 'admin'

@app.route("/", methods=['GET'])
def home():
    return render_template('admin.html')

@app.route("/AddAdmin", methods=['POST'])
def addAdmin():
    adm_id = request.form['adm_id']
    adm_first_name = request.form['adm_first_name']
    adm_last_name = request.form['adm_last_name']
    adm_location = request.form['adm_location']
    adm_img = request.files['adm_img']

    cursor = db_conn.cursor()
    insert_sql = "INSERT INTO admin_profile(adm_id, adm_first_name, adm_last_name, adm_location) VALUES (%s, %s, %s, %s)"

    if adm_img == "":
        return "Please select a image"

    try:
        cursor.execute(insert_sql, (adm_id, adm_first_name, adm_last_name, adm_location))
        db_conn.commit()

        # Uplaod image file in S3 #
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

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM admin_profile')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('admin_profile.html', rows=rows)

@app.route("/StudentApplyJobs", methods=['GET'])
def student_apply_jobs():
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM student')
    rows = cursor.fetchall()
    cursor.close()
    return render_template('StudentApplyJobs.html', rows=rows)

@app.route("/companylistadm", methods=['GET'])
def company_list():
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM company')
    rows = cursor.fetchall()
    cursor.close()
    return render_template('company_list_adm.html', rows=row)

@app.route("/assignsupervisor", methods=['POST'])
def assign_supervisor():
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

    return render_template('assign_supervisor_Output.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)



