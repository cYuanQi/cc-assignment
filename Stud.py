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
table = 'student'

@app.route("/")
def home():
    return render_template('user_page.html')

@app.route("/nologin")
def nologin():
    return render_template('no_login.html')
    
@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/joblistings")
def joblistings():
    return render_template('job-listings.html')

@app.route("/jobsingle")
def jobsingle():
    return render_template('job-single.html')

@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/servicesingle")
def servicesingle():
    return render_template('service-single.html')

@app.route("/blog")
def blog():
    return render_template('blog.html')

@app.route("/blogsingle")
def blogsingle():
    return render_template('blog-single.html')

@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')

@app.route("/portfoliosingle")
def portfoliosingle():
    return render_template('portfolio-single.html')

@app.route("/testimonials")
def testimonials():
    return render_template('testimonials.html')

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/gallery")
def gallery():
    return render_template('gallery.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/studentreport")
def studentreport():
    return render_template('Student_report.html')

@app.route("/studentdetails")
def studentdetails():
    return render_template('student-details.html')

@app.route("/userpage")
def userpage():
    return render_template('user_page.html')

@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/studentapplyjobs")
def studentapplyjobs():
    return render_template('StudentApplyJobs.html')

@app.route("/companylistadm")
def companylistadm():
    return render_template('company_list_adm.html')

@app.route("/assignsupervisor")
def assignsupervisor():
    return render_template('assign-supervisor.html')

@app.route("/postjob")
def postjob():
    return render_template('post-job.html')