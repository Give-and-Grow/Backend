from app.models.opportunity_participant import OpportunityParticipant, ParticipantStatus
from app.models.opportunity import Opportunity
from app.models.volunteer_opportunity import VolunteerOpportunity
from app.models.opportunity_day import OpportunityDay
from sqlalchemy.orm import joinedload

def check_schedule_conflict(user_id: int, target_opportunity: Opportunity):
    if not target_opportunity.volunteer_details:
        return False  # فقط فرص التطوع عندها أوقات

    target_details = target_opportunity.volunteer_details
    target_days = {d.day_of_week for d in target_details.days}
    target_start = target_details.start_time
    target_end = target_details.end_time

    user_participations = OpportunityParticipant.query.options(
        joinedload(OpportunityParticipant.opportunity)
        .joinedload(Opportunity.volunteer_details)
        .joinedload(VolunteerOpportunity.days)
    ).filter(
        OpportunityParticipant.user_id == user_id,
        OpportunityParticipant.status.in_([ParticipantStatus.PENDING, ParticipantStatus.ACCEPTED])
    ).all()

    for participation in user_participations:
        existing_opp = participation.opportunity
        if not existing_opp or not existing_opp.volunteer_details:
            continue

        # تحقق من تقاطع التاريخ
        if not (target_opportunity.end_date < existing_opp.start_date or target_opportunity.start_date > existing_opp.end_date):
            existing_details = existing_opp.volunteer_details
            existing_days = {d.day_of_week for d in existing_details.days}

            if target_days.intersection(existing_days):
                existing_start = existing_details.start_time
                existing_end = existing_details.end_time
                if not (target_end <= existing_start or target_start >= existing_end):
                    return True  # يوجد تعارض

    return False  # لا يوجد تعارض
