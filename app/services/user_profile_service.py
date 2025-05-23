#Backend/app/services/user_profile_service.py
from bcrypt import checkpw
from marshmallow import ValidationError

from ..extensions import db
from ..models.account import Account, Role
from ..models.admin_details import AdminDetails
from ..models.organization_details import OrganizationDetails
from ..models.skill import Skill
from ..models.user_details import UserDetails
from ..schemas.user_schema import (
    ChangePasswordSchema,
    UpdateAdminProfileSchema,
    UpdateOrgProfileSchema,
    UpdateUserProfileSchema,
)
from ..utils.duration_since import get_duration_since
from ..utils.location import get_lat_lon_from_location

def get_own_profile_service(account_id):
    account = Account.query.get(account_id)
    if not account:
        return {"msg": "Account not found"}, 404

    response = {
        "email": account.email,
        "username": account.username,
        "role": account.role.value,
        "is_email_verified": account.is_email_verified,
        "registration_duration": get_duration_since(account.created_at),
    }

    if account.role == Role.USER:
        user_details = UserDetails.query.filter_by(
            account_id=account_id
        ).first()
        if not user_details:
            return {"msg": "User details not found"}, 404
        response.update(
            {
                "name": user_details.first_name,
                "last_name": user_details.last_name,
                "phone_number": user_details.phone_number,
                "gender": (
                    user_details.gender.value if user_details.gender else None
                ),
                "date_of_birth": (
                    user_details.date_of_birth.strftime("%Y-%m-%d")
                    if user_details.date_of_birth
                    else None
                ),
                "country": user_details.country,
                "city": user_details.city,
                "village": user_details.village,
                
                "bio": user_details.bio,
                "profile_picture": user_details.profile_picture,
                "experience": user_details.experience,
                "skills": [{"id": skill.id, "name": skill.name} for skill in user_details.skills],
                "identity_verification_status": (
                    user_details.identity_verification_status.value
                    if user_details.identity_verification_status
                    else None
                ),
            }
        )
    elif account.role == Role.ORGANIZATION:
        org_details = OrganizationDetails.query.filter_by(
            account_id=account_id
        ).first()
        if not org_details:
            return {"msg": "Organization details not found"}, 404
        response.update(
            {
                "name": org_details.name,
                "description": org_details.description,
                "phone": org_details.phone,
                "logo": org_details.logo,
                "address": org_details.address,
                "verified": org_details.proof_verification_status.value,
            }
        )
    elif account.role == Role.ADMIN:
        admin_details = AdminDetails.query.filter_by(
            account_id=account_id
        ).first()
        if not admin_details:
            return {"msg": "Admin details not found"}, 404
        response.update(
            {
                "name": admin_details.name,
                "role_level": admin_details.role_level.value,
            }
        )

    return response, 200


def update_profile_service(account_id, data):
    try:
        account = Account.query.get(account_id)
        if not account:
            return {"msg": "Account not found"}, 404

        if account.role == Role.USER:
            schema = UpdateUserProfileSchema()
        elif account.role == Role.ORGANIZATION:
            schema = UpdateOrgProfileSchema()
        elif account.role == Role.ADMIN:
            schema = UpdateAdminProfileSchema()
        else:
            return {"msg": "Invalid role"}, 400

        validated_data = schema.load(data)

        new_username = validated_data.get("username")
        if new_username and new_username != account.username:
            if Account.query.filter(
                Account.username == new_username, Account.id != account_id
            ).first():
                return {
                    "msg": f"Username '{new_username}' is already taken"
                }, 400
            account.username = new_username

        if account.role == Role.USER:
            user_details = UserDetails.query.filter_by(
                account_id=account_id
            ).first()
            if not user_details:
                return {"msg": "User details not found"}, 404
            
            location_fields = ["country", "city", "village"]
            location_parts = [validated_data.get(field) for field in location_fields if validated_data.get(field)]
            location_string = ", ".join(location_parts) if location_parts else None

            if location_string:
                coords = get_lat_lon_from_location(location_string)
                if coords:
                    validated_data["latitude"] = coords["latitude"]
                    validated_data["longitude"] = coords["longitude"]

            for field in [
                "first_name",
                "last_name",
                "phone_number",
                "gender",
                "country",
                "city",
                "village",
                "bio",
                "experience",
                "date_of_birth",
                "profile_picture",
                "identity_picture",
                "latitude",
                "longitude",
            ]:
                if (
                    field in validated_data
                    and getattr(user_details, field) != validated_data[field]
                ):
                    setattr(user_details, field, validated_data[field])

            if "skills" in validated_data:
                new_skills = validated_data["skills"]
                user_details.skills.clear()
                for skill_name in new_skills:
                    skill = Skill.query.filter_by(name=skill_name).first()
                    if not skill:
                        skill = Skill(name=skill_name)
                        db.session.add(skill)
                    user_details.skills.append(skill)

        elif account.role == Role.ORGANIZATION:
            org_details = OrganizationDetails.query.filter_by(
                account_id=account_id
            ).first()
            if not org_details:
                return {"msg": "Organization details not found"}, 404
            for field in ["name", "description", "phone", "logo", "address"]:
                if (
                    field in validated_data
                    and getattr(org_details, field) != validated_data[field]
                ):
                    setattr(org_details, field, validated_data[field])

        elif account.role == Role.ADMIN:
            admin_details = AdminDetails.query.filter_by(
                account_id=account_id
            ).first()
            if not admin_details:
                return {"msg": "Admin details not found"}, 404
            for field in ["name", "role_level"]:
                if (
                    field in validated_data
                    and getattr(admin_details, field) != validated_data[field]
                ):
                    setattr(admin_details, field, validated_data[field])

        db.session.commit()
        return {"msg": "Profile updated successfully"}, 200

    except ValidationError as ve:
        return {"msg": "Validation error", "errors": ve.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {"msg": "An error occurred", "error": str(e)}, 500


def change_password_service(account_id, data):
    try:
        schema = ChangePasswordSchema()
        validated_data = schema.load(data)

        old_password = validated_data.get("old_password")
        new_password = validated_data.get("new_password")

        account = Account.query.get(account_id)
        if not account:
            return {"message": "Account not found"}, 404

        if not checkpw(
            old_password.encode("utf-8"), account.password.encode("utf-8")
        ):
            return {"message": "Old password is incorrect"}, 400

        account.set_password(new_password)
        db.session.commit()

        return {
            "status": "success",
            "message": "Password changed successfully",
        }, 200

    except ValidationError as ve:
        return {"message": "Validation error", "errors": ve.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {"message": "An error occurred", "error": str(e)}, 500
