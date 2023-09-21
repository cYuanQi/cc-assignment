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
    insert_sql = "INSERT INTO adm_profile(adm_id, adm_name, adm_gender, adm_dob, adm_address, adm_email, adm_phone) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    if not adm_img:
        return "Please select an image"

    try:
        cursor.execute(insert_sql, (adm_id, adm_name, adm_gender, adm_dob, adm_address, adm_email, adm_phone))
        db_conn.commit()

        # Check if the uploaded file is a JPG image
        if adm_img.filename == '':
            return "Please select a file"

        if not adm_img.filename.endswith('.jpg'):
            return "Please upload a PNG image"

        # Generate a secure filename and save the image file
        adm_file_name_in_s3 = "adm-id-" + str(adm_id) + "_image_file.jpg"
        adm_img.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(adm_file_name_in_s3)))

        # Save the image file name in the database
        update_sql = "UPDATE adm_profile SET adm_image = %s WHERE adm_id = %s"
        cursor.execute(update_sql, (adm_file_name_in_s3, adm_id))
        db_conn.commit()

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

    # Now, you can query the admin_list table to get data
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM admin_list')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('admin_list.html', rows=rows)

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
