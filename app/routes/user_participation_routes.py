from flask import Blueprint, request, jsonify, g
from app.models.opportunity import Opportunity
from app.services.user_participation_service import UserParticipantService
from app.utils.decorators import account_required
from flask_jwt_extended import jwt_required, get_jwt_identity
user_participation_bp = Blueprint("user_participant", __name__)

@user_participation_bp.route('/<int:opportunity_id>/join', methods=['POST'])
@jwt_required()
def join_opportunity(opportunity_id):
    user_id = get_jwt_identity()
    return UserParticipantService.join_opportunity(user_id, opportunity_id)


@user_participation_bp.route("<int:opportunity_id>/withdraw", methods=["POST"])
@jwt_required()
def withdraw_application(opportunity_id):
    user_id = get_jwt_identity()     
    return UserParticipantService.withdraw_from_opportunity(user_id, opportunity_id)


@user_participation_bp.route("/applications", methods=["GET"])
@account_required
def get_user_applications():
    user_id = g.user_id

    applications = UserParticipantService.get_user_applications(user_id)

    if isinstance(applications, tuple):  # Error returned from service
        response, status_code = applications
        return jsonify(response), status_code

    if not applications:
        return jsonify({"message": "No applications found"}), 404

    return jsonify(applications), 200

@user_participation_bp.route("/evaluate", methods=["POST"])
@account_required
def evaluate_participation():
    data = request.json
    user_id = g.user_id
    participant_id = data.get("participant_id")
    rating = data.get("rating")
    feedback = data.get("feedback")

    if not participant_id or not rating:
        return jsonify({"error": "participant_id and rating are required"}), 400

    result = UserParticipantService.evaluate_participation(user_id, participant_id, rating, feedback)

    if isinstance(result, tuple):
        response, status_code = result
        return jsonify(response), status_code

    return jsonify(result), 200
