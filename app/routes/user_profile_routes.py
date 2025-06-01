#Backend/app/routes/user_profile.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..services.user_profile_service import (
    change_password_service,
    get_own_profile_service,
    update_profile_service,
    verify_identity_with_ocr_service,
)

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/", methods=["GET"])
@jwt_required()
def get_own_profile():
    account_id = get_jwt_identity()
    response, status = get_own_profile_service(account_id)
    return jsonify(response), status

@profile_bp.route("/", methods=["PUT"])
@jwt_required()
def update_profile():
    account_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400
    response, status = update_profile_service(account_id, data)
    return jsonify(response), status


@profile_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():
    account_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400
    response, status = change_password_service(account_id, data)
    return jsonify(response), status

@profile_bp.route("/verify-identity", methods=["POST"])
@jwt_required()
def verify_identity():
    account_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'image_url' not in data:
        return jsonify({"message": "Image URL is required"}), 400

    image_url = data["image_url"]

    response, status = verify_identity_with_ocr_service(account_id, image_url)
    return jsonify(response), status
