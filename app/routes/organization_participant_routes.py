from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.organization_participant_services import *

op_participant_bp = Blueprint("op_participant", __name__)

@op_participant_bp.get("/<int:opportunity_id>/participants")
@jwt_required()
def get_participants(opportunity_id):
    org_id = get_jwt_identity()
    return get_opportunity_participants(opportunity_id, org_id)

@op_participant_bp.post("/<int:opportunity_id>/participants")
@jwt_required()
def bulk_update_participant_status(opportunity_id):
    org_id = get_jwt_identity()
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Request body must be a list of status updates"}), 400

    return bulk_change_participant_status(opportunity_id, org_id, data)

@op_participant_bp.post("/<int:opportunity_id>/participants/<int:user_id>/status")
@jwt_required()
def update_participant_status(opportunity_id, user_id):
    org_id = get_jwt_identity()
    new_status = request.json.get("status")

    if not new_status:
        return jsonify({"error": "Missing status field"}), 400

    return change_participant_status(opportunity_id, user_id, org_id, new_status)

@op_participant_bp.get("/my-organization/applications")
@jwt_required()
def get_all_applications_for_organization():
    org_id = get_jwt_identity()
    return fetch_all_applications_for_organization(org_id)
