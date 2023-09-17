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

@app.route("/StudentApplyJobs", methods=['GET'])
def student_apply_jobs():
    return render_template('StudentApplyJobs.html')

@app.route("/company_list_adm", methods=['GET'])
def company_list():
    return render_template('company_list_adm.html')

@app.route("/assign-supervisor", methods=['POST'])
def assign_supervisor():
    stud_name = request.form['stud_name']
    stud_id = request.form['stud_id']
    sup_name = request.form['sup_name']
    sup_id = request.form['sup_id']

    cursor = db_conn.cursor()
    insert_sql = "INSERT INTO admin VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_sql, (stud_name, stud_id, sup_name, sup_id))
    db_conn.commit()
    cursor.close()


    return render_template('assign_supervisor_Output.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)




