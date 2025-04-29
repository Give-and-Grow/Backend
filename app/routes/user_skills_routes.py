# Backend/app/routes/user_skills_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user_details import UserDetails
from ..models.skill import Skill
from ..extensions import db

user_skills_bp = Blueprint("user_skills", __name__)


@user_skills_bp.route("/", methods=["GET"])
@jwt_required()
def get_my_skills():
    current_user_id = get_jwt_identity()
    user = UserDetails.query.filter_by(account_id=current_user_id).first()
    if not user:
        return jsonify({"error": "User not found."}), 404

    skills = [{"id": skill.id, "name": skill.name} for skill in user.skills]
    return jsonify({"skills": skills}), 200


@user_skills_bp.route("/add", methods=["POST"])
@jwt_required()
def add_skill_to_profile():
    current_user_id = get_jwt_identity()
    user = UserDetails.query.filter_by(account_id=current_user_id).first()
    if not user:
        return jsonify({"error": "User not found."}), 404

    data = request.get_json()
    skill_id = data.get("skill_id")

    if not skill_id:
        return jsonify({"error": "Skill ID is required."}), 400

    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": "Skill not found."}), 404

    if skill in user.skills:
        return jsonify({"message": "Skill already added to profile."}), 400

    user.skills.append(skill)
    db.session.commit()

    return jsonify({"message": f"Skill '{skill.name}' added to profile."}), 201


@user_skills_bp.route("/remove", methods=["POST"])
@jwt_required()
def remove_skill_from_profile():
    current_user_id = get_jwt_identity()
    user = UserDetails.query.filter_by(account_id=current_user_id).first()
    if not user:
        return jsonify({"error": "User not found."}), 404

    data = request.get_json()
    skill_id = data.get("skill_id")

    if not skill_id:
        return jsonify({"error": "Skill ID is required."}), 400

    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": "Skill not found."}), 404

    if skill not in user.skills:
        return jsonify({"message": "Skill not associated with your profile."}), 400

    user.skills.remove(skill)
    db.session.commit()

    return jsonify({"message": f"Skill '{skill.name}' removed from profile."}), 200

@user_skills_bp.route("/add/<int:skill_id>", methods=["POST"])
@jwt_required()
def add1_skill_to_profile(skill_id):
    current_user_id = get_jwt_identity()
    user = UserDetails.query.filter_by(account_id=current_user_id).first()
    if not user:
        return jsonify({"error": "User not found."}), 404

    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": "Skill not found."}), 404

    if skill in user.skills:
        return jsonify({"message": "Skill already added to profile."}), 400

    user.skills.append(skill)
    db.session.commit()

    return jsonify({"message": f"Skill '{skill.name}' added to profile."}), 201


@user_skills_bp.route("/remove/<int:skill_id>", methods=["DELETE"])
@jwt_required()
def remove1_skill_from_profile(skill_id):
    current_user_id = get_jwt_identity()
    user = UserDetails.query.filter_by(account_id=current_user_id).first()
    if not user:
        return jsonify({"error": "User not found."}), 404

    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": "Skill not found."}), 404

    if skill not in user.skills:
        return jsonify({"message": "Skill not associated with your profile."}), 400

    user.skills.remove(skill)
    db.session.commit()

    return jsonify({"message": f"Skill '{skill.name}' removed from profile."}), 200

@user_skills_bp.route("/available", methods=["GET"])
@jwt_required()
def get_available_skills():
    current_user_id = get_jwt_identity()
    user = UserDetails.query.filter_by(account_id=current_user_id).first()
    if not user:
        return jsonify({"error": "User not found."}), 404

    # Get all skills
    all_skills = Skill.query.all()
    # Get skills already associated with the user
    user_skills = set(user.skills)
    
    # Filter skills not yet added to user's profile
    available_skills = [
        {"id": skill.id, "name": skill.name}
        for skill in all_skills if skill not in user_skills
    ]

    return jsonify({"available_skills": available_skills}), 200