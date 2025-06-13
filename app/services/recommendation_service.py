#Backend/app/services/recommendation_service.py
from flask import request
from app.models.account import Account, Role
from app.models.user_details import UserDetails
from app.models.opportunity import OpportunityType
from app.ml.recommender import recommend_opportunities_for_user
from app.services.opportunity_service import OpportunityService

from sqlalchemy import func
from app.extensions import db
from app.models.follow import Follow
from app.models.account import Account
from app.models.user_details import UserDetails
from app.models.organization_details import OrganizationDetails

class RecommendationService:
    @staticmethod
    def get_recommended_opportunities(account_id):
        account = Account.query.get(account_id)
        if not account:
            return {"error": "Account not found"}, 404

        if account.role != Role.USER:
            return {"error": "Unauthorized role"}, 403

        user_details = UserDetails.query.filter_by(account_id=account_id).first()
        if not user_details:
            return {"error": "User details not found"}, 404

        opportunity_type_param = request.args.get("type", None)
        opportunity_type_enum = None
        if opportunity_type_param:
            opportunity_type_param = opportunity_type_param.lower()
            if opportunity_type_param not in ["volunteer", "job"]:
                return {"error": "Invalid opportunity type"}, 400
            opportunity_type_enum = (
                OpportunityType.VOLUNTEER if opportunity_type_param == "volunteer" else OpportunityType.JOB
            )
        limit = int(request.args.get("limit", 100))
        opportunities = recommend_opportunities_for_user(user_details.id, opportunity_type_enum, limit)

        if not opportunities:
            return {"error": "No opportunities found"}, 404

        serialized = [OpportunityService.serialize_opportunity(opp) for opp in opportunities]
        return serialized, 200
    
import random
from sqlalchemy.sql.expression import func

def get_follow_recommendations(user_id, limit=5):
    followed_subquery = db.session.query(Follow.followed_id).filter(
        Follow.follower_id == user_id
    ).subquery()

    similar_users_subquery = db.session.query(Follow.follower_id).filter(
        Follow.followed_id.in_(followed_subquery),
        Follow.follower_id != user_id
    ).distinct().subquery()

    recommended_query = db.session.query(
        Follow.followed_id,
        func.count(Follow.follower_id).label('score')
    ).filter(
        Follow.follower_id.in_(similar_users_subquery),
        ~Follow.followed_id.in_(followed_subquery),
        Follow.followed_id != user_id
    ).group_by(Follow.followed_id).order_by(func.count(Follow.follower_id).desc()).limit(limit)

    recommended_ids = [row.followed_id for row in recommended_query]

    if not recommended_ids:
        fixed_user_id = 39
        all_candidate_ids_query = db.session.query(Account.id).filter(
            Account.id != user_id  
        )
        all_candidate_ids = [row.id for row in all_candidate_ids_query]
        if fixed_user_id in all_candidate_ids:
            all_candidate_ids.remove(fixed_user_id)
            random_ids = random.sample(all_candidate_ids, min(limit - 1, len(all_candidate_ids)))
            recommended_ids = [fixed_user_id] + random_ids
        else:
            recommended_ids = random.sample(all_candidate_ids, min(limit, len(all_candidate_ids)))
    accounts = Account.query.filter(Account.id.in_(recommended_ids)).all()

    results = []

    for account in accounts:
        if account.role.value == "user" and account.user_details:
            full_name = f"{account.user_details.first_name} {account.user_details.last_name}"
            results.append({
                "id": account.id,
                "role": account.role.value,
                "username": account.username,
                "name": full_name,
                "profile_picture": account.user_details.profile_picture
            })
        elif account.role.value == "organization" and account.organization_details:
            results.append({
                "id": account.id,
                "role": account.role.value,
                "username": account.username,
                "name": account.organization_details.name,
                "profile_picture": account.organization_details.logo
            })

    return results
