from flask import Blueprint, request, jsonify
from app.services.opportunity_service import OpportunityService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import organization_required
from app.utils.distance import haversine_distance
from app.models.opportunity import Opportunity
from app.models.user_details import UserDetails  
from app.extensions import db

opportunity_bp = Blueprint('opportunity_bp', __name__)

@opportunity_bp.route('/create', methods=['POST'])
@jwt_required()
def create_opportunity():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    return OpportunityService.create_opportunity(current_user_id,data)
    
@opportunity_bp.route('/<int:opportunity_id>', methods=['GET'])
def get_opportunity(opportunity_id):
    return OpportunityService.get_opportunity(opportunity_id)

@opportunity_bp.route('/list', methods=['GET'])
def list_opportunities():
    filters = request.args  
    return OpportunityService.list_opportunities(filters)

@opportunity_bp.route('/<int:opportunity_id>', methods=['PUT'])
@jwt_required()
def update_opportunity(opportunity_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    return OpportunityService.update_opportunity(current_user_id, opportunity_id, data)

@opportunity_bp.route('/<int:opportunity_id>', methods=['DELETE'])
@jwt_required()
def delete_opportunity(opportunity_id):
    current_user_id = get_jwt_identity()
    return OpportunityService.delete_opportunity(current_user_id, opportunity_id)

@opportunity_bp.route('/<int:opportunity_id>/restore', methods=['PUT'])
@jwt_required()
def restore_opportunity(opportunity_id):
    current_user_id = get_jwt_identity()
    return OpportunityService.restore_opportunity(current_user_id, opportunity_id)


@opportunity_bp.route('/organization', methods=['GET'])
@jwt_required()
def get_opportunities_by_organization():
    current_user_id = get_jwt_identity()
    filters = request.args 
    return OpportunityService.get_opportunities_by_organization(current_user_id, filters)


@opportunity_bp.route('/<int:opportunity_id>/change-status', methods=['PATCH'])
@jwt_required()
def change_status(opportunity_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    status = data.get('status')
    if not status:
        return {"msg": "Missing 'status' in request data"}, 400
    
    return OpportunityService.change_status(current_user_id, opportunity_id, status)


@opportunity_bp.route("/nearby_opportunities", methods=["GET"])
@jwt_required()
def get_nearby_opportunities():
    current_user_id = get_jwt_identity()
    max_distance_km = float(request.args.get("max_distance", 50))  
    return OpportunityService.get_nearby_opportunities(current_user_id, max_distance_km)
