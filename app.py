from flask import *
from functions import *
import math

app = Flask(__name__)

@app.route('/')
def home():

    locations = get_locations()
    jobType = get_jobType()
    salaryRange = get_salaryRange()
    companies, total_records = get_companies(page=1, per_page=5)  # Initial load, first 5 companies
    total_pages = (total_records + 4) // 5  # Calculate total pages (5 items per page)
    featured_jobs = get_featured_jobs()
    return render_template('home.html', locations=locations, jobtypes=jobType, salaryranges=salaryRange, companies=companies, total_pages=total_pages, postedjobs = featured_jobs)


@app.route('/search', methods=['POST'])
def search():
    job_title = request.form.get('job_title')
    location = request.form.get('location')
    job_type = request.form.get('job_type')
    salary_range = request.form.get('search_salary')
    page = int(request.form.get('currentPage', 1))

    if location == "None" or location == "Select Location":
        location = None
    if job_type == "None" or location == "Job Type":
        job_type = None
    
    featured_jobs = get_featured_jobs(job_title=job_title, location=location, job_type=job_type, salary_range=salary_range)
    print(page)
    # print(job_title)
    # print(location)
    print(job_type)
    # print(salary_range)
    per_page = 2
    pages = math.ceil(len(featured_jobs) / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = featured_jobs[start:end]
    
    return jsonify({'htmlresponse': render_template('components/response.html', postedjobs=paginated_data, page = page, per_page =per_page, total = pages  )})



@app.route('/find-jobs')
def findJobs():
    return render_template('find-jobs.html')

@app.route('/find-talent')
def findTalent():
    return render_template('find-talent.html')

@app.route('/choose')
def choose():
    return render_template('choose.html')

@app.route('/candidate/register')
def candidateReg():
    return render_template('candidate/register.html')

@app.route('/candidate/login')
def candidateLogin():
    return render_template('candidate/login.html')

@app.route('/company/register')
def companyReg():
    return render_template('company/register.html')

@app.route('/company/login')
def companyLogin():
    return render_template('company/login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/signin')

# comment

if __name__ == '__main__':
    app.debug = True
    app.run()