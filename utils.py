from datetime import datetime, timedelta
import pytz
import pymysql

def time_ago(date):
    if date is None:
        return 'recently'
    
    now = datetime.now(pytz.utc)
    diff = now - date

    if diff.days >= 365:
        years = diff.days // 365
        return f'{years} Yr' if years > 1 else '1 Yr'
    elif diff.days >= 30:
        months = diff.days // 30
        return f'{months} M' if months > 1 else '1 M'
    elif diff.days > 0:
        return f'{diff.days} Day' if diff.days > 1 else '1 Day'
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f'{hours} Hr' if hours > 1 else '1 Hr'
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f'{minutes} Min' if minutes > 1 else '1 Min'
    else:
        return 'Now'

def get_featured_jobs(job_title=None, location=None, job_type=None, salary_range=None):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    query = """
    SELECT companies.company_name, companies.company_logo, postedjobs.job_title,postedjobs.updated_at,
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
    for job in featured_jobs:
        job = list(job)
        if isinstance(job[3], str):
            job[5] = datetime.strptime(job[5], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)
        elif isinstance(job[3], datetime):
            job[3] = job[3].replace(tzinfo=pytz.utc)
        job[3] = time_ago(job[3])
        #print(datetime.strptime(job[3], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc))
        updated.append(job)
    cursor.close()
    connection.close()
    return updated
