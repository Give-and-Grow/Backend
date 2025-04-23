# Backend/app/services/admin_organization_services.py
from app.extensions import db
from app.models.organization_details import (
    OrganizationDetails,
    VerificationStatus,
)
from app.schemas.organization_schema import OrganizationProfileSchema


def get_pending_organizations():
    pending_orgs = OrganizationDetails.query.filter_by(
        proof_verification_status=VerificationStatus.PENDING
    ).all()
    schema = OrganizationProfileSchema(many=True)
    return schema.dump(pending_orgs), 200


def get_organization_by_id(org_id):
    org = OrganizationDetails.query.get(org_id)
    if not org:
        return {"msg": "Organization not found"}, 404

    schema = OrganizationProfileSchema()
    return schema.dump(org), 200


def update_organization_status(org_id, status):
    org = OrganizationDetails.query.get(org_id)
    if not org:
        return {"msg": "Organization not found"}, 404

    if org.proof_verification_status == status:
        return {"msg": f"Organization already {status.value}"}, 200

    try:
        org.proof_verification_status = status
        db.session.commit()
        return {"msg": f"Organization {status.value}"}, 200
    except Exception as e:
        db.session.rollback()
        return {"msg": "Database error", "error": str(e)}, 500

def get_all_organizations(status=None):
    query = OrganizationDetails.query
    if status:
        try:
            status_enum = VerificationStatus[status.upper()]
            query = query.filter_by(proof_verification_status=status_enum)
        except KeyError:
            return {"msg": "Invalid status filter"}, 400

    orgs = query.all()
    schema = OrganizationProfileSchema(many=True)
    return schema.dump(orgs), 200

def remove_organization(org_id):
    org = OrganizationDetails.query.get(org_id)
    if not org:
        return {"msg": "Organization not found"}, 404
    try:
        db.session.delete(org)
        db.session.commit()
        return {"msg": "Organization deleted"}, 200
    except Exception as e:
        db.session.rollback()
        return {"msg": "Database error", "error": str(e)}, 500


