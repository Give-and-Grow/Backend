#Backend/app/services/recommendation_service.py
from flask import request
from app.models.account import Account, Role
from app.models.user_details import UserDetails
from app.models.opportunity import OpportunityType
from app.ml.recommender import recommend_opportunities_for_user

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

        return opportunities, 200
