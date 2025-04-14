from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_duration_since(date):
    if not date:
        return None
    now = datetime.utcnow()
    diff = relativedelta(now, date)

    parts = []
    if diff.years:
        parts.append(f"{diff.years} year{'s' if diff.years > 1 else ''}")
    if diff.months:
        parts.append(f"{diff.months} month{'s' if diff.months > 1 else ''}")
    if diff.days:
        parts.append(f"{diff.days} day{'s' if diff.days > 1 else ''}")

    return ", ".join(parts) if parts else "Today"
