# Backend/app/routes/organization.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from ..schemas.organization_schema import (
    IndustryListSchema,
    IndustryOutputSchema,
    OrganizationProfileSchema,
    OrganizationUpdateSchema,
)
from ..services.organization_service import (
    add_industries_to_organization,
    get_organization_profile,
    remove_industry_from_organization,
    replace_organization_industries,
    update_organization_profile,
    validate_and_add_industries
)

organization_bp = Blueprint("organization", __name__)


@organization_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    response, status = get_organization_profile()
    if status == 200:
        schema = OrganizationProfileSchema()
        return jsonify(schema.dump(response)), 200
    return jsonify(response), status


@organization_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "No data provided"}), 400

    try:
        valid_data = OrganizationUpdateSchema().load(data)
    except ValidationError as err:
        return jsonify({"msg": "Invalid data", "errors": err.messages}), 400

    response, status = update_organization_profile(valid_data)
    return jsonify(response), status


@organization_bp.route("/industries", methods=["GET"])
@jwt_required()
def get_industries():
    response, status = get_organization_profile()
    if status == 200:
        industries = response.industries
        schema = IndustryOutputSchema(many=True)
        return jsonify(schema.dump(industries)), 200
    return jsonify(response), status


@organization_bp.route("/industries", methods=["POST"])
@jwt_required()
def add_industries():
    data = request.get_json()
    try:
        valid_data = IndustryListSchema().load(data)
    except ValidationError as err:
        return jsonify({"msg": "Invalid data", "errors": err.messages}), 400

    response, status = validate_and_add_industries(valid_data["industry_ids"])
    return jsonify(response), status


@organization_bp.route("/industries", methods=["PUT"])
@jwt_required()
def update_industries():
    data = request.get_json()
    industry_ids = data.get("industry_ids")
    if not industry_ids or not isinstance(industry_ids, list):
        return jsonify({"msg": "industry_ids must be a list"}), 400
    response, status = replace_organization_industries(industry_ids)
    return jsonify(response), status


@organization_bp.route("/industries/<int:industry_id>", methods=["DELETE"])
@jwt_required()
def delete_industry(industry_id):
    response, status = remove_industry_from_organization(industry_id)
    return jsonify(response), status
