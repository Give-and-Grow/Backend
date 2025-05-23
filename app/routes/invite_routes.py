from flask import Blueprint, jsonify
from app.services.recommend_cf import recommend_users_for_org

invite_recommendation_bp = Blueprint("recommendation", __name__)

@invite_recommendation_bp.route("/opportunity/<int:opportunity_id>/invite", methods=["POST"])
def invite_top_users(opportunity_id):
    from app.services.recommend_cf import recommend_users_for_org
    from app.services.invite import invite_recommended_users

    opportunity = Opportunity.query.get(opportunity_id)
    if not opportunity:
        return {"error": "Opportunity not found"}, 404

    recommended = recommend_users_for_org(opportunity.org_id, top_n=5)
    invite_recommended_users(opportunity_id, recommended)

    return jsonify({"invited_user_ids": recommended})