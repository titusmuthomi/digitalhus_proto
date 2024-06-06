from flask import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

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

if __name__ == '__main__':
    app.debug = True
    app.run()