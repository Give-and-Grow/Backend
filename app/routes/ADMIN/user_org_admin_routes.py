#Backend/app/routes/ADMIN/user_org_admin_routes.py
from flask import Blueprint, request
from app.services.ADMIN.user_org_admin_services import *
from sqlalchemy import Enum as SqlEnum
from app.models.user_details import UserDetails, VerificationStatus as UserVerificationStatus
from app.models.organization_details import OrganizationDetails, VerificationStatus 



admin_user_bp = Blueprint("admin_user_bp", __name__, url_prefix="/admin/users")
admin_org_bp = Blueprint("admin_org_bp", __name__, url_prefix="/admin/organizations")
admin_admin_bp = Blueprint("admin_admin_bp", __name__, url_prefix="/admin/admins")

# ========================= USERS ========================= #

@admin_user_bp.route("/", methods=["GET"])
def get_all_users():
    return get_all_users_service(request)

@admin_user_bp.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    return get_user_service(user_id)

@admin_user_bp.route("/identity", methods=["GET"])
def get_identity_for_all_users():
    users = UserDetails.query.filter(
        UserDetails.identity_verification_status == VerificationStatus.PENDING.value,  
        UserDetails.identity_picture.isnot(None),
        UserDetails.identity_picture != ""
    ).all()

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "full_name": f"{user.first_name} {user.last_name}",
            "gender": user.gender.value if user.gender else None,
            "city": user.city,
            "identity_picture": user.identity_picture,
            "verification_status": user.identity_verification_status.value,
        })
    return jsonify(result), 200 

@admin_user_bp.route("/identity/<int:user_id>/verification", methods=["PUT"])
def update_verification_status(user_id):
    data = request.get_json()
    new_status = data.get("status")  

    if new_status not in [status.value for status in UserVerificationStatus]:
        return jsonify({"error": "Invalid status"}), 400

    user = UserDetails.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.identity_verification_status = UserVerificationStatus(new_status)
    db.session.commit()

    return jsonify({"message": "Verification status updated successfully"}), 200

@admin_user_bp.route("/stats", methods=["GET"])
def get_user_stats():
    return get_user_stats_service()

# ====================== ORGANIZATIONS ===================== #

@admin_org_bp.route("/", methods=["GET"])
def get_all_organizations():
    return get_all_organizations_service(request)

@admin_org_bp.route("/<int:org_id>", methods=["GET"])
def get_organization_by_id(org_id):
    return get_organization_service(org_id)

@admin_org_bp.route("/proof", methods=["GET"])
def get_pending_proof_for_organizations():
    organizations = OrganizationDetails.query.filter(
        OrganizationDetails.proof_verification_status == VerificationStatus.PENDING.value,
        OrganizationDetails.proof_image.isnot(None),
        OrganizationDetails.proof_image != ""
    ).all()

    result = []
    for org in organizations:
        result.append({
            "id": org.id,
            "name": org.name,
            "phone": org.phone,
            "address": org.address,
            "proof_image": org.proof_image,
            "verification_status": org.proof_verification_status.value,
        })
    return jsonify(result), 200

@admin_org_bp.route("/proof/<int:org_id>/status", methods=["PUT"])
def update_proof_verification_status(org_id):
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in [status.value for status in VerificationStatus]:
        return jsonify({"error": "Invalid status value"}), 400

    org = OrganizationDetails.query.get(org_id)
    if not org:
        return jsonify({"error": "Organization not found"}), 404

    org.proof_verification_status = VerificationStatus(new_status)
    db.session.commit()

    return jsonify({"message": "Verification status updated successfully"}), 200
    
@admin_org_bp.route("/stats", methods=["GET"])
def get_organization_stats():
    return get_organization_stats_service()

# ========================== ADMINS ========================= #

@admin_admin_bp.route("/", methods=["GET"])
def get_all_admins():
    return get_all_admins_service(request)

@admin_admin_bp.route("/<int:admin_id>", methods=["GET"])
def get_admin_by_id(admin_id):
    return get_admin_service(admin_id)

@admin_admin_bp.route("/stats", methods=["GET"])
def get_admin_stats():
    return get_admin_stats_service()
