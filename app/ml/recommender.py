# Backend/app/ml/recommender.py
from app.models import UserDetails, Opportunity
from app.models.opportunity import OpportunityType
from app.extensions import db

def get_user_skills(user_id):
    user = UserDetails.query.get(user_id)
    if not user:
        return set()
    return set(skill.id for skill in user.skills)

from datetime import date
from app.models import UserDetails, Opportunity
from app.models.opportunity import OpportunityType, OpportunityStatus
from app.extensions import db

def get_user_skills(user_id):
    user = UserDetails.query.get(user_id)
    if not user:
        return set()
    return set(skill.id for skill in user.skills)

def recommend_opportunities_for_user(user_id, opportunity_type=None, limit=10):
    user_skill_ids = get_user_skills(user_id)
    if not user_skill_ids:
        return []

    today = date.today()

    query = Opportunity.query.filter_by(is_deleted=False, status=OpportunityStatus.OPEN)
    query = query.filter(Opportunity.start_date >= today)

    if opportunity_type:
        query = query.filter_by(opportunity_type=opportunity_type)

    all_opportunities = query.all()
    recommendations = []

    for opportunity in all_opportunities:
        opp_skill_ids = set(skill.id for skill in opportunity.skills)
        if not opp_skill_ids:
            continue

        common_skills = user_skill_ids.intersection(opp_skill_ids)
        score = len(common_skills) / len(opp_skill_ids)

        if score > 0:
            recommendations.append((opportunity, score))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return [op.to_dict() for op, _ in recommendations[:limit]]
