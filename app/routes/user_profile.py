from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.user_profile_service import (
    get_own_profile_service,
    update_profile_service,
    change_password_service
)

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/', methods=['GET'])
@jwt_required()
def get_own_profile():
    account_id = get_jwt_identity()
    response, status = get_own_profile_service(account_id)
    return jsonify(response), status

@profile_bp.route('/', methods=['PUT'])
@jwt_required()
def update_profile():
    account_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    response, status = update_profile_service(account_id, data)
    return jsonify(response), status

@profile_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    account_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    response, status = change_password_service(account_id, data)
    return jsonify(response), status