import mysql.connector
# Database configuration
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'hustle_db'
}

db_config2 = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'test'
}

def get_locations():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT location_name FROM locations")
    locations = cursor.fetchall()
    cursor.close()
    connection.close()
    return locations

def get_jobType():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT jobtype_name FROM jobtypes")
    type = cursor.fetchall()
    cursor.close()
    connection.close()
    return type

def get_salaryRange():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT salary_range FROM salaryranges")
    range = cursor.fetchall()
    cursor.close()
    connection.close()
    return range

def get_companies(page=1, per_page=5):
    offset = (page - 1) * per_page
    connection = mysql.connector.connect(**db_config2)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM companies")
    total_records = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM companies LIMIT %s OFFSET %s", (per_page, offset))
    companies = cursor.fetchall()
    cursor.close()
    connection.close()
    return companies, total_records


def get_jobs():
    sql = '''
    SELECT companies.company_name, companies.company_email, postedjobs.job_title, jobtypes.jobtype_name, locations.location_name FROM ( (postedjobs INNER JOIN companies ON postedjobs.company_id = companies.id) INNER JOIN locations ON companies.id = locations.id) INNER JOIN jobtypes ON companies.id = jobtypes.id
       '''