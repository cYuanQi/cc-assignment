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

@app.route("/admin", methods=['GET'])
def home():
    return render_template('admin.html')

@app.route("/AddAdmin", methods=['POST'])
def addAdmin():
    return render_template('AddAdmin.html')


@app.route("/companylistadm", methods=['GET'])
def company_list():
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM company')
    rows = cursor.fetchall()
    cursor.close()
    return render_template('company_list_adm.html', rows=row)


@app.route("/assignsupervisor", methods=['GET', 'POST'])
def assign_supervisor():
    return render_template('assign-supervisor.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)



