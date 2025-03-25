from flask import Blueprint, request, jsonify
from ..services.auth_service import signup_service, login_service, verify_service, reset_password_request_service, reset_password_service
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    response, status = signup_service(name, email, password)
    return jsonify(response), status

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    response, status = login_service(username, password)
    return jsonify(response), status

@auth_bp.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    code = data.get('code')
    response, status = verify_service(code)
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