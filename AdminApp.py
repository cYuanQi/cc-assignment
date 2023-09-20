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

@app.route("/")
def home():
    return render_template('admin.html')

@app.route("/admin", methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route("/addadmin", methods=['GET'])
def addAdmin():
    return render_template('addadmin.html')


@app.route("/companylistadm", methods=['GET'])
def company_list():
    return render_template('company_list_adm.html')


@app.route("/assignsupervisor", methods=['GET'])
def assign_supervisor():
    return render_template('assign-supervisor.html')
    
@app.route("/nologin", methods = ['GET'])
def nologin():
    return render_template('no_login.html')
    
@app.route("/jobsingle", methods = ['GET'])
def jobsingle():
    return render_template('job-single.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)



