from datetime import datetime, timedelta, date
from app.models.opportunity_participant import OpportunityParticipant
from app.models.participant_attendance import AttendanceStatus

WEEKDAY_MAP = {
    "sunday": 6,
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5
}

def calculate_volunteer_hours(opportunity, user_id, db_session):
    volunteer_info = opportunity.volunteer_details
    if not volunteer_info:
        return None

    working_days = [WEEKDAY_MAP[day.day_of_week.value] for day in volunteer_info.days]

    daily_hours = (
        datetime.combine(date.today(), volunteer_info.end_time) -
        datetime.combine(date.today(), volunteer_info.start_time)
    ).seconds / 3600

    current_day = opportunity.start_date
    total_working_days = 0
    while current_day <= opportunity.end_date:
        if current_day.weekday() in working_days:
            total_working_days += 1
        current_day += timedelta(days=1)

    total_hours = total_working_days * daily_hours
    # استعلام عن مشاركة اليوزر في الفرصة
    participant = db_session.query(OpportunityParticipant).filter_by(
        opportunity_id=opportunity.id,
        user_id=user_id
    ).first()

    if not participant:
        return None

    # احسب الساعات بناءً على سجلات الحضور
    attended_hours = 0
    for record in participant.attendance_records:
        if record.status == AttendanceStatus.PRESENT:
            attended_hours += daily_hours
        elif record.status == AttendanceStatus.LATE:
            attended_hours += daily_hours * 0.5

    missed_hours = max(total_hours - attended_hours, 0)

    return {
        "total_hours": total_hours,
        "attended_hours": attended_hours,
        "missed_hours": missed_hours
    }
