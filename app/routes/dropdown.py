#Backend/app/routes/dropdown.py
from flask import Blueprint, jsonify
from app.services.dropdown_services import DropdownService

dropdown_bp = Blueprint('dropdown', __name__, url_prefix='/api/dropdown')

@dropdown_bp.route('/opportunity-status', methods=['GET'])
def get_opportunity_status_options():
    return jsonify(DropdownService.get_opportunity_status_options()), 200
