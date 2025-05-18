#GAG/app/routes/dropdown.py
from flask import Blueprint, jsonify
from app.services.dropdown_services import DropdownService

dropdown_bp = Blueprint('dropdown', __name__)

@dropdown_bp.route('/roles', methods=['GET'])
def get_roles():
    roles = DropdownService.get_roles()
    return jsonify(roles), 200

@dropdown_bp.route('/admin-roles', methods=['GET'])
def get_admin_roles():
    admin_roles = DropdownService.get_admin_roles()
    return jsonify(admin_roles), 200

@dropdown_bp.route('/industries', methods=['GET'])
def get_industries():
    industries = DropdownService.get_industries()
    return jsonify(industries), 200

@dropdown_bp.route('/week-days', methods=['GET'])
def get_week_days():
    days = DropdownService.get_week_days()
    return jsonify(days), 200

@dropdown_bp.route('/participant-statuses', methods=['GET'])
def get_participant_statuses():
    statuses = DropdownService.get_participant_statuses()
    return jsonify(statuses), 200

@dropdown_bp.route('/opportunity-statuses', methods=['GET'])
def get_opportunity_statuses():
    statuses = DropdownService.get_opportunity_statuses()
    return jsonify(statuses), 200

@dropdown_bp.route('/opportunity-types', methods=['GET'])
def get_opportunity_types():
    types = DropdownService.get_opportunity_types()
    return jsonify(types), 200 

@dropdown_bp.route('/verification-statuses', methods=['GET'])
def get_verification_statuses():
    statuses = DropdownService.get_verification_statuses()
    return jsonify(statuses), 200

@dropdown_bp.route('/attendance-statuses', methods=['GET'])
def get_attendance_statuses():
    statuses = DropdownService.get_attendance_statuses()
    return jsonify(statuses), 200

@dropdown_bp.route('/skills', methods=['GET'])
def get_skills():
    skills = DropdownService.get_skills()
    return jsonify(skills), 200

@dropdown_bp.route('/tags', methods=['GET'])
def get_tags():
    tags = DropdownService.get_tags()
    return jsonify(tags), 200
@dropdown_bp.route('/achievements', methods=['GET'])
def get_achievements():
    achievements = DropdownService.get_achievement_types()
    return jsonify(achievements), 200
@dropdown_bp.route('/levels', methods=['GET'])
def get_levels():
    levels = DropdownService.get_levels()
    return jsonify(levels), 200
@dropdown_bp.route('/rankings', methods=['GET'])
def get_rankings():
    rankings = DropdownService.get_rankings()
    return jsonify(rankings), 200

@dropdown_bp.route('/genders', methods=['GET'])
def get_genders():
    genders = DropdownService.get_genders()
    return jsonify(genders), 200

@dropdown_bp.route('/period-types', methods=['GET'])
def get_period_types():
    period_types = DropdownService.get_period_types()
    return jsonify(period_types), 200
