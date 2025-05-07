#Backend/app/routes/recommendation.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.recommendation_service import RecommendationService 

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
