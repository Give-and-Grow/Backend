# Backend/app/services/organization_service.py
from flask_jwt_extended import get_jwt_identity

from ..extensions import db
from ..models.account import Account, Role
from ..models.industry import Industry
from ..models.organization_details import OrganizationDetails
from sqlalchemy.orm import joinedload
from app.schemas.organization_schema import OrganizationProfileSchema
from app.models.organization_details import VerificationStatus

def get_current_organization():
    current_user_id = get_jwt_identity()
    account = Account.query.get(current_user_id)
    if not account or account.role != Role.ORGANIZATION:
        return None, {"msg": "Unauthorized or invalid role"}, 403

    org = OrganizationDetails.query.filter_by(account_id=account.id).first()
    if not org:
        return None, {"msg": "Organization profile not found"}, 404

    return org, None, 200


def get_organization_profile():
    current_user_id = get_jwt_identity()

    organization = (
        db.session.query(OrganizationDetails)
        .join(Account)
        .filter(Account.id == current_user_id)
        .first()
    )

    if organization:
        return organization, 200
    return {"msg": "Organization not found"}, 404


def update_organization_profile(data):
    org, error, status = get_current_organization()
    if error:
        return error, status

    updatable_fields = [
        "name",
        "description",
        "phone",
        "address",
        "logo",
        "proof_image",
    ]
    for field in updatable_fields:
        if field in data:
            setattr(org, field, data[field])

    db.session.commit()
    return {"msg": "Organization profile updated successfully"}, 200


def add_industries_to_organization(industry_ids):
    org, error, status = get_current_organization()
    if error:
        return error, status

    industries = Industry.query.filter(Industry.id.in_(industry_ids)).all()
    org.industries.extend([i for i in industries if i not in org.industries])
    db.session.commit()
    return {"msg": "Industries added successfully"}, 200


def replace_organization_industries(industry_ids):
    org, error, status = get_current_organization()
    if error:
        return error, status

    unique_ids = list(set(industry_ids))

    existing_industries = Industry.query.filter(Industry.id.in_(unique_ids)).all()
    existing_ids = {ind.id for ind in existing_industries}
    invalid_ids = [i for i in unique_ids if i not in existing_ids]

    if invalid_ids:
        return {
            "msg": "Some industry IDs are invalid",
            "invalid_ids": invalid_ids
        }, 400

    org.industries = existing_industries
    db.session.commit()

    return {"msg": "Industries updated successfully"}, 200



def remove_industry_from_organization(industry_id):
    org, error, status = get_current_organization()
    if error:
        return error, status

    industry = db.session.get(Industry, industry_id)
    if not industry:
        return {"msg": f"Industry with ID {industry_id} not found"}, 404

    if industry not in org.industries:
        return {"msg": "Industry not associated with this organization"}, 404

    org.industries.remove(industry)
    db.session.commit()
    return {"msg": "Industry removed successfully"}, 200



def get_filtered_organizations(
    name="", industry_id=None,phone="", description="", verified=None, page=1, limit=10
):
    query = OrganizationDetails.query.options(
        joinedload(OrganizationDetails.industries)
    )

    if name:
        query = query.filter(OrganizationDetails.name.ilike(f"%{name}%"))

    if industry_id:
        query = query.filter(
            OrganizationDetails.industries.any(id=industry_id)
        )

    if phone:
        query = query.filter(OrganizationDetails.phone.ilike(f"%{phone}%"))

    if description:
        query = query.filter(OrganizationDetails.description.ilike(f"%{description}%"))

    if verified is not None:
        if verified.lower() == "true":
            query = query.filter(
                OrganizationDetails.proof_verification_status
                == VerificationStatus.APPROVED
            )
        elif verified.lower() == "false":
            query = query.filter(
                OrganizationDetails.proof_verification_status
                != VerificationStatus.APPROVED
            )

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    organizations = pagination.items

    schema = OrganizationProfileSchema(many=True)
    return (
        schema.dump(organizations),
        pagination.total,
        pagination.page,
        pagination.pages,
    )


def validate_and_add_industries(industry_ids):
    org, error, status = get_current_organization()
    if error:
        return error, status

    unique_industry_ids = list(set(industry_ids))  

    existing_industries = Industry.query.filter(Industry.id.in_(unique_industry_ids)).all()
    existing_ids = {ind.id for ind in existing_industries}
    invalid_ids = [i for i in unique_industry_ids if i not in existing_ids]

    if invalid_ids:
        return {
            "msg": "Some industry IDs are invalid",
            "invalid_ids": invalid_ids
        }, 400

    industries_to_add = [
        industry for industry in existing_industries if industry not in org.industries
    ]

    if not industries_to_add:
        return {
            "msg": "All industries are already added to the organization."
        }, 400

    org.industries.extend(industries_to_add)

    db.session.commit()
    return {"msg": "Industries added successfully"}, 200

