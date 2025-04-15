from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..services.auth_service import (
    signup_service,
    login_service,
    verify_service,
    resend_code_service,
    reset_password_request_service,
    reset_password_service,
    logout_service,
    get_users_by_year_service
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])

def signup():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "No data provided"}), 400

    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password or not role:
        return jsonify({"msg": "Email, password, and role are required"}), 400
    data.pop('email', None)
    data.pop('password', None)
    data.pop('role', None)
    response, status = signup_service(email=email, password=password, role=role, **data)
    return jsonify(response), status

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('username')
    password = data.get('password')
    response, status = login_service(email, password)
    return jsonify(response), status

@auth_bp.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    response, status = verify_service(email, code)
    return jsonify(response), status

@auth_bp.route('/resend-code', methods=['POST'])
def resend_code():
    data = request.get_json()
    email = data.get('email')
    response, status = resend_code_service(email)
    return jsonify(response), status

@auth_bp.route('/reset-password-request', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    email = data.get('email')
    response, status = reset_password_request_service(email)
    return jsonify(response), status

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    code = data.get('code')
    new_password = data.get('new_password')
    response, status = reset_password_service(code, new_password)
    return jsonify(response), status

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response, status = logout_service()
    return jsonify(response), status

@auth_bp.route('/users/<int:year>', methods=['GET'])
@jwt_required()
def get_users_by_year(year):
    response, status = get_users_by_year_service(year)
    return jsonify(response), status