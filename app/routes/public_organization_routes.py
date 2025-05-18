#Backend/app/routes/public_organization.py
from app.services.organization_service import get_filtered_organizations
from app.schemas.organization_schema import OrganizationProfileSchema
from flask import Blueprint, jsonify, request
from app.models.account import Account


from app.extensions import db
from app.models.organization_details import (
    OrganizationDetails,
    VerificationStatus,
)



public_org_bp = Blueprint("public_organization", __name__)


@public_org_bp.route("/", methods=["GET"])
def list_organizations():
    name = request.args.get("name", "", type=str)
    phone = request.args.get("phone", "", type=str)  
    description = request.args.get("description", "", type=str)  
    industry_id = request.args.get("industry", type=int)
    verified = request.args.get("verified", type=str)
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)


    organizations, total, current_page, total_pages = (
        get_filtered_organizations(
            name=name,
            phone=phone,  
            description=description,  
            industry_id=industry_id,
            verified=verified,
            page=page,
            limit=limit,
        )
    )

    return (
        jsonify(
            {
                "results": organizations,
                "total": total,
                "page": current_page,
                "pages": total_pages,
            }
        ),
        200,
    )


@public_org_bp.route("/<string:username>", methods=["GET"])
def get_organization_by_username(username):
    accounts = Account.query.filter(Account.username.ilike(f"%{username}%")).all()

    if not accounts:
        return jsonify({"msg": "No organizations found"}), 404

    results = []
    schema = OrganizationProfileSchema()
    for account in accounts:
        if account.organization_details:
            results.append(schema.dump(account.organization_details))

    if not results:
        return jsonify({"msg": "No organizations with profiles found"}), 404

    return jsonify(results), 200


@public_org_bp.route("/by-name/<string:name>", methods=["GET"])
def get_organization_by_name(name):
    organizations = OrganizationDetails.query.filter(
        OrganizationDetails.name.ilike(f"%{name}%")
    ).all()
    if not organizations:
        return jsonify({"msg": "No organizations found with that name"}), 404

    schema = OrganizationProfileSchema(many=True)
    return jsonify(schema.dump(organizations)), 200
