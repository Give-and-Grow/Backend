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
        return {"msg": "Internal server error"}, 500
