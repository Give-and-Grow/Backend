from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.schemas.opportunity_participant_schema import RatingInputSchema
from app.services.opportunity_participant_service import OpportunityService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.account import Account, Role

opportunity_participant_bp = Blueprint("opportunity_participant", __name__)

@opportunity_participant_bp.route("/<int:participant_id>/rate", methods=["POST"])
@jwt_required()
def rate_participant(participant_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()

    current_account = Account.query.get(current_user_id)
    if not current_account or current_account.role != Role.ORGANIZATION:
        return {"msg": "Only an organization can rate participants"}, 403

    return OpportunityService.rate_participant(current_user_id, participant_id, data)

@opportunity_participant_bp.route('/opportunities/<int:opportunity_id>/participants', methods=['GET'])
@jwt_required()
def get_opportunity_participants(opportunity_id):
    result = OpportunityService.get_participants_by_opportunity(opportunity_id)
    if isinstance(result, tuple):
        data, status = result
        return jsonify(data), status
    return jsonify(result), 200

@opportunity_participant_bp.route('/opportunities/<int:opportunity_id>/join', methods=['POST'])
@jwt_required()
def join_opportunity(opportunity_id):
    user_id = get_jwt_identity()
    return OpportunityService.join_opportunity(user_id, opportunity_id)

@opportunity_participant_bp.route('/opportunities/<int:opportunity_id>/withdraw', methods=['POST'])
@jwt_required()
def withdraw_from_opportunity(opportunity_id):
    
    user_id = get_jwt_identity()
    return OpportunityService.withdraw_from_opportunity(user_id, opportunity_id)

@opportunity_participant_bp.route('/opportunities/<int:opportunity_id>/check-participation', methods=['GET'])
@jwt_required()
def check_participation(opportunity_id):
    user_id = get_jwt_identity()
    return OpportunityService.check_participation(user_id, opportunity_id)