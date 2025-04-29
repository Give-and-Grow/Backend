from flask import Blueprint, request, jsonify
from app.services.opportunity_service import OpportunityService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import organization_required

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
    filters = request.args  # يمكنك تمرير فلترة بالـ query string
    return OpportunityService.list_opportunities(filters)

# @opportunity_bp.route('/<int:opportunity_id>/update', methods=['PUT'])
# @jwt_required()
# def update_opportunity(opportunity_id):
#     current_user_id = get_jwt_identity()
#     data = request.get_json()
#     return OpportunityService.update_opportunity(current_user_id, opportunity_id, data)

# @opportunity_bp.route('/<int:opportunity_id>/delete', methods=['DELETE'])
# @jwt_required()
# def delete_opportunity(opportunity_id):
#     current_user_id = get_jwt_identity()
#     return OpportunityService.delete_opportunity(current_user_id, opportunity_id)

# @opportunity_bp.route('/<int:opportunity_id>/change-status', methods=['PATCH'])
# @jwt_required()
# def change_status(opportunity_id):
#     current_user_id = get_jwt_identity()
#     data = request.get_json()
#     return OpportunityService.change_status(current_user_id, opportunity_id, data.get('status'))
