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

