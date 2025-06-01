from flask import request, jsonify
from app.models.user_details import UserDetails
from app.models.organization_details import OrganizationDetails
from app.models.admin_details import AdminDetails, AdminRoleLevel
from app.models.opportunity import Opportunity
from app.extensions import db
from sqlalchemy import func, or_

# ===================== USERS =====================
def get_all_users_service(req):
    page = int(req.args.get("page", 1))
    per_page = int(req.args.get("per_page", 10))
    search = req.args.get("search", "").strip()

    query = UserDetails.query
    if search:
        query = query.join(UserDetails.account).filter(
            or_(
                UserDetails.first_name.ilike(f"%{search}%"),
                UserDetails.last_name.ilike(f"%{search}%"),
                UserDetails.city.ilike(f"%{search}%")
            )
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    users = pagination.items

    result = [
        {
            "id": user.id,
            "full_name": f"{user.first_name} {user.last_name}",
            "email": user.account.email,
            "phone_number": user.phone_number,
            "city": user.city,
            "total_points": user.total_points,
            "verification_status": user.identity_verification_status.value
        }
        for user in users
    ]
    return jsonify({
        "items": result,
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }), 200

def get_user_service(user_id):
    user = UserDetails.query.get_or_404(user_id)
    data = {
        "id": user.id,
        "full_name": f"{user.first_name} {user.last_name}",
        "email": user.account.email,
        "phone_number": user.phone_number,
        "city": user.city,
        "bio": user.bio,
        "experience": user.experience,
        "points": {
            "total": user.total_points,
            "current": user.current_points
        },
        "verification_status": user.identity_verification_status.value,
        "skills": [skill.name for skill in user.skills]
    }
    return jsonify(data), 200

def get_user_stats_service():
    total_users = UserDetails.query.count()

    users_by_city = db.session.query(UserDetails.city, func.count(UserDetails.id)).group_by(UserDetails.city).all()
    users_by_gender = db.session.query(UserDetails.gender, func.count(UserDetails.id)).group_by(UserDetails.gender).all()
    pending_users = UserDetails.query.filter_by(identity_verification_status="PENDING").count()

    stats = {
        "total_users": total_users,
        "pending_users": pending_users,
        "users_by_city": [{"city": city, "count": count} for city, count in users_by_city],
        "users_by_gender": [{"gender": gender.value, "count": count} for gender, count in users_by_gender],

       
    }
    return jsonify(stats), 200

# ===================== ORGANIZATIONS =====================
def get_all_organizations_service(req):
    page = int(req.args.get("page", 1))
    per_page = int(req.args.get("per_page", 10))
    search = req.args.get("search", "").strip()

    query = OrganizationDetails.query
    if search:
        query = query.join(OrganizationDetails.account).filter(
            or_(
                OrganizationDetails.name.ilike(f"%{search}%"),
                OrganizationDetails.phone.ilike(f"%{search}%"),
                OrganizationDetails.account.email.ilike(f"%{search}%")
            )
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    orgs = pagination.items

    result = [
        {
            "id": org.id,
            "name": org.name,
            "email": org.account.email,
            "phone": org.phone,
            "is_active": org.is_active,
            "verification_status": org.proof_verification_status.value
        }
        for org in orgs
    ]
    return jsonify({
        "items": result,
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }), 200

def get_organization_service(org_id):
    org = OrganizationDetails.query.get_or_404(org_id)
    data = {
        "id": org.id,
        "name": org.name,
        "email": org.account.email,
        "phone": org.phone,
        "description": org.description,
        "address": org.address,
        "is_active": org.is_active,
        "verification_status": org.proof_verification_status.value
    }
    return jsonify(data), 200

def get_organization_stats_service():
    total_orgs = OrganizationDetails.query.count()
    active_orgs = OrganizationDetails.query.filter_by(is_active=True).count()
    inactive_orgs = total_orgs - active_orgs
    verified_orgs = OrganizationDetails.query.filter_by(proof_verification_status="APPROVED").count()


    stats = {
        "total_organizations": total_orgs,
        "active_organizations": active_orgs,
        "inactive_organizations": inactive_orgs,
        "verified_organizations": verified_orgs
    }
    return jsonify(stats), 200

# ===================== ADMINS =====================
def get_all_admins_service(req):
    page = int(req.args.get("page", 1))
    per_page = int(req.args.get("per_page", 10))
    search = req.args.get("search", "").strip()

    query = AdminDetails.query
    if search:
        query = query.join(AdminDetails.account).filter(
            or_(
                AdminDetails.name.ilike(f"%{search}%"),
                AdminDetails.account.email.ilike(f"%{search}%")
            )
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    admins = pagination.items

    result = [
        {
            "id": admin.id,
            "name": admin.name,
            "email": admin.account.email,
            "role_level": admin.role_level.value,
            "is_active": admin.is_active
        }
        for admin in admins
    ]
    return jsonify({
        "items": result,
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }), 200

def get_admin_service(admin_id):
    admin = AdminDetails.query.get_or_404(admin_id)
    data = {
        "id": admin.id,
        "name": admin.name,
        "email": admin.account.email,
        "role_level": admin.role_level.value,
        "is_active": admin.is_active
    }
    return jsonify(data), 200

def get_admin_stats_service():
    total_admins = AdminDetails.query.count()
    active_admins = AdminDetails.query.filter_by(is_active=True).count()
    inactive_admins = total_admins - active_admins
    admin_rolels =[
        {"role": role.value, "count": AdminDetails.query.filter_by(role_level=role).count()}
        for role in AdminRoleLevel
    ]

    stats = {
        "roles": admin_rolels,
        "total_admins": total_admins,
        "active_admins": active_admins,
        "inactive_admins": inactive_admins
    }
    return jsonify(stats), 200