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

@app.route("/admin")
def home():
    return render_template('admin.html')

@app.route("/addadmin", methods=['GET', 'POST'])
def addAdmin():
    return render_template('addadmin.html')


@app.route("/companylistadm", methods=['GET', 'POST'])
def company_list():
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM company')
    rows = cursor.fetchall()
    cursor.close()
    return render_template('company_list_adm.html', rows=row)


@app.route("/assignsupervisor", methods=['GET', 'POST'])
def assign_supervisor():
    return render_template('assign-supervisor.html')

@app.route("/assignsupervisorProcess", methods=['POST'])
def assign_supervisorProcess():
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



