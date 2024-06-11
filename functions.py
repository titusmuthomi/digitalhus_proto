import pymysql
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
    'database': 'hustle_db'
}

def get_locations():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT location_name FROM locations")
    locations = cursor.fetchall()
    cursor.close()
    connection.close()
    return locations

def get_jobType():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT id, jobtype_name FROM jobtypes")
    type = cursor.fetchall()
    cursor.close()
    connection.close()
    return type

def get_salaryRange():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT id, salary_range FROM salaryranges")
    range = cursor.fetchall()
    cursor.close()
    connection.close()
    return range

# def get_featured_jobs():
#     connection = pymysql.connect(**db_config)
#     cursor = connection.cursor()
#     cursor.execute("SELECT companies.company_name, companies.company_logo, postedjobs.job_title, jobtypes.jobtype_name, locations.location_name, GROUP_CONCAT( skills.skill_name SEPARATOR',') as skills FROM postedjobs LEFT JOIN companies ON postedjobs.company_id = companies.id left JOIN locations ON locations.id = postedjobs.job_location_id LEFT JOIN jobtypes ON jobtypes.id = postedjobs.jobtype_id LEFT JOIN postedjobs_skills ON postedjobs.id = postedjobs_skills.posted_job_id LEFT JOIN skills ON skills.id = postedjobs_skills.skill_id GROUP BY companies.company_name, companies.company_logo, postedjobs.job_title, jobtypes.jobtype_name, locations.location_name")
#     featured_jobs = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return featured_jobs


def get_featured_jobs(job_title=None, location=None, job_type=None, salary_range=None):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    query = """
    SELECT companies.company_name, companies.company_logo, postedjobs.job_title,
           jobtypes.jobtype_name, locations.location_name,
           GROUP_CONCAT(skills.skill_name SEPARATOR ',') as skills
    FROM postedjobs
    LEFT JOIN companies ON postedjobs.company_id = companies.id
    LEFT JOIN locations ON locations.id = postedjobs.job_location_id
    LEFT JOIN jobtypes ON jobtypes.id = postedjobs.jobtype_id
    LEFT JOIN postedjobs_skills ON postedjobs.id = postedjobs_skills.posted_job_id
    LEFT JOIN skills ON skills.id = postedjobs_skills.skill_id
    WHERE 1=1
    """

    params = []
    if job_title:
        query += " AND postedjobs.job_title LIKE %s"
        params.append(f"%{job_title}%")
    if location:
        query += " AND locations.location_name = %s"
        params.append(location)
    if job_type:
        query += " AND jobtypes.id = %s"
        params.append(job_type)
    if salary_range:
        query += " AND postedjobs.salary_range_id = %s"
        params.append(salary_range)

    query += " GROUP BY companies.company_name, companies.company_logo, postedjobs.job_title, postedjobs.updated_at, jobtypes.jobtype_name, locations.location_name"

    cursor.execute(query, params)
    updated = []
    featured_jobs = cursor.fetchall()
    cursor.close()
    connection.close()
    return updated


def get_companies(page=1, per_page=5):
    offset = (page - 1) * per_page
    connection = pymysql.connect(**db_config)
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