# Backend/app/routes/admin_organization.py
from flask import Blueprint, jsonify, request
from app.utils.decorators import admin_required
from app.models.organization_details import VerificationStatus

from ..services.admin_organization_services import (
    get_organization_by_id,
    get_pending_organizations,
    update_organization_status,
    get_all_organizations,
    remove_organization,
)

admin_org_bp = Blueprint("admin_organization", __name__)


@admin_org_bp.route("/pending", methods=["GET"])
@admin_required
def list_pending_organizations():
    data, status = get_pending_organizations()
    return jsonify(data), status


@admin_org_bp.route("/<int:org_id>", methods=["GET"])
@admin_required
def get_organization_details(org_id):
    data, status = get_organization_by_id(org_id)
    if status == 404:
        return jsonify({"msg": "Organization not found"}), 404
    return jsonify(data), 200


@admin_org_bp.route("/<int:org_id>/approve", methods=["PUT"])
@admin_required
def approve_organization(org_id):
    data, status = update_organization_status(org_id, VerificationStatus.APPROVED)
    return jsonify(data), status


@admin_org_bp.route("/<int:org_id>/reject", methods=["PUT"])
@admin_required
def reject_organization(org_id):
    data, status = update_organization_status(org_id, VerificationStatus.REJECTED)
    return jsonify(data), status

@admin_org_bp.route("/all", methods=["GET"])
@admin_required
def list_all_organizations():
    status = request.args.get("status")
    data, response_status = get_all_organizations(status)
    return jsonify(data), response_status

@admin_org_bp.route("/<int:org_id>", methods=["DELETE"])
@admin_required
def delete_organization(org_id):
    data, status = remove_organization(org_id)
    return jsonify(data), status

