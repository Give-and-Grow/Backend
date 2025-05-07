#Backend/app/routes/dropdown.py
from flask import Blueprint, jsonify
from app.services.dropdown_services import DropdownService

dropdown_bp = Blueprint('dropdown', __name__, url_prefix='/api/dropdown')

@dropdown_bp.route('/opportunity-status', methods=['GET'])
def get_opportunity_status_options():
    return jsonify(DropdownService.get_opportunity_status_options()), 200

@dropdown_bp.route('/opportunity-type', methods=['GET'])
def get_opportunity_type_options():
    return jsonify(DropdownService.get_opportunity_type_options()), 200

@dropdown_bp.route('/verification-status', methods=['GET'])
def get_verification_status_options():
    return jsonify(DropdownService.get_verification_status_options()), 200

@dropdown_bp.route('/report-status', methods=['GET'])
def get_report_status_options():
    return jsonify(DropdownService.get_report_status_options()), 200

@dropdown_bp.route('/attendance-status', methods=['GET'])
def get_attendance_status_options():
    return jsonify(DropdownService.get_attendance_status_options()), 200
