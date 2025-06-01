#Backend/app/services/ADMIN/admin_opportunity_stats_service.py
from flask import jsonify
from sqlalchemy import func
from app.extensions import db
from app.models import  Opportunity, OrganizationDetails
from app.models.opportunity_day import OpportunityDay, WeekDay
from app.models.opportunity import OpportunityType, OpportunityStatus
from app.models.opportunity_participant import ParticipantStatus
from sqlalchemy import extract

def get_opportunity_counts_by_type():
    data = (
        db.session.query(Opportunity.opportunity_type, func.count(Opportunity.id))
        .group_by(Opportunity.opportunity_type)
        .all()
    )
    result = {op_type.value: count for op_type, count in data}
    return jsonify({"opportunity_counts_by_type": result})

def get_opportunity_counts_by_status():
    data = (
        db.session.query(Opportunity.status, func.count(Opportunity.id))
        .group_by(Opportunity.status)
        .all()
    )
    result = {status.value: count for status, count in data}
    return jsonify({"opportunity_counts_by_status": result})



def get_top_organizations_by_opportunity_count(limit=5):
    data = (
        db.session.query(OrganizationDetails.name, func.count(Opportunity.id).label("count"))
        .join(Opportunity, OrganizationDetails.id == Opportunity.organization_id)
        .group_by(OrganizationDetails.id)
        .order_by(func.count(Opportunity.id).desc())
        .limit(limit)
        .all()
    )
    result = [{"organization": name, "opportunity_count": count} for name, count in data]
    return jsonify({"top_organizations": result})

def get_least_active_organizations(limit=5):
    subquery = (
        db.session.query(Opportunity.organization_id, func.count(Opportunity.id).label("count"))
        .group_by(Opportunity.organization_id)
        .subquery()
    )
    data = (
        db.session.query(OrganizationDetails.name, func.coalesce(subquery.c.count, 0))
        .outerjoin(subquery, OrganizationDetails.id == subquery.c.organization_id)
        .order_by(func.coalesce(subquery.c.count, 0).asc())
        .limit(limit)
        .all()
    )
    result = [{"organization": name, "opportunity_count": count} for name, count in data]
    return jsonify({"least_active_organizations": result})

def get_opportunity_count_by_month():
    raw_results = (
        db.session.query(
            extract('month', Opportunity.start_date).label('month'),
            func.count(Opportunity.id).label('count')
        )
        .filter(Opportunity.is_deleted == False)
        .group_by('month')
        .all()
    )

    result_map = {int(month): count for month, count in raw_results}

    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    data = [
        {
            "month": month_names[i],
            "opportunity_count": result_map.get(i + 1, 0)
        }
        for i in range(12)
    ]

    return jsonify({"opportunities_by_month": data})

def get_volunteer_opportunity_count_by_weekday():
  
    result = (
        db.session.query(
            OpportunityDay.day_of_week,
            func.count(OpportunityDay.id).label("count")
        )
        .group_by(OpportunityDay.day_of_week)
        .all()
    )
    day_order = [
        WeekDay.SUNDAY, WeekDay.MONDAY, WeekDay.TUESDAY, WeekDay.WEDNESDAY,
        WeekDay.THURSDAY, WeekDay.FRIDAY, WeekDay.SATURDAY
    ]
    result_map = {day.name.lower(): 0 for day in day_order}
    for day, count in result:
        result_map[day.value] = count

    data = [
        {"day": day.value.capitalize(), "opportunity_count": result_map[day.value]}
        for day in day_order
    ]

    return jsonify({"volunteer_opportunities_by_day": data})

from app.models.opportunity import Opportunity
from app.models.opportunity_participant import OpportunityParticipant
from app.models.organization_details import OrganizationDetails

def get_organization_participation_stats(limit=10):
    result = (
        db.session.query(
            OrganizationDetails.name.label("organization_name"),
            func.count(OpportunityParticipant.id).label("participant_count")
        )
        .join(Opportunity, Opportunity.organization_id == OrganizationDetails.id)
        .join(OpportunityParticipant, Opportunity.id == OpportunityParticipant.opportunity_id)
        .filter(OpportunityParticipant.status == ParticipantStatus.ACCEPTED)
        .group_by(OrganizationDetails.id)
        .order_by(func.count(OpportunityParticipant.id).desc())
        .limit(limit)
        .all()
    )

    data = [
        {
            "organization_name": org_name,
            "participant_count": count
        } for org_name, count in result
    ]

    return jsonify({"top_organizations_by_participation": data})
