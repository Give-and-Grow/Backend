from flask import Blueprint, jsonify
from app.services.user_service import UserService

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/profile/<int:user_id>", methods=["GET"])
def get_user_profile(user_id):
    profile_data = UserService.get_user_profile_summary(user_id)
    return jsonify(profile_data)
