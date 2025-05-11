#Backend/app/routes/recommendation.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.recommendation_service import RecommendationService 
from app.models.opportunity import Opportunity
from app.extensions import db

recommendation_bp = Blueprint("recommendation_bp", __name__)

@recommendation_bp.route("/opportunities", methods=["GET"])
@jwt_required()
def recommend():
    try:
        account_id = get_jwt_identity()
        opportunities, status = RecommendationService.get_recommended_opportunities(account_id)

        if status != 200:
            return jsonify({"msg": opportunities["error"]}), status

        return jsonify(opportunities), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"msg": "Internal server error"}, 500

@recommendation_bp.route("/CFopportunities", methods=["GET"])
@jwt_required()
def recommend_cf():
    account_id = get_jwt_identity()
    if not account_id:
        return jsonify({"error": "user_id is required"}), 400

    opportunity_ids = RecommendationService.recommend_opportunities_for_user_cf(account_id)

    
    opportunities = Opportunity.query.filter(Opportunity.id.in_(opportunity_ids)).all()

    return jsonify([opp.to_dict() for opp in opportunities])

@recommendation_bp.route("/CFsimilar_users", methods=["GET"])
@jwt_required()
def similar_users_cf():
    account_id = get_jwt_identity()
    if not account_id:
        return jsonify({"error": "user_id is required"}), 400

    similar_users = RecommendationService.get_similar_users(account_id)

    return jsonify(similar_users)