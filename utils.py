from datetime import datetime, timedelta
import pytz

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