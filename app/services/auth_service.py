#Backend/app/services/auth_service.py
# Built-in imports
import random
import string
from secrets import choice
from datetime import datetime, timedelta, timezone

from bcrypt import checkpw

# Third-party imports
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from marshmallow import ValidationError
from sqlalchemy import extract, or_

# App-level imports (Flask app structure)
from app.extensions import db
from app.models.account import Account, Role
from app.models.admin_details import AdminDetails, AdminRoleLevel
from app.models.organization_details import OrganizationDetails
from app.models.token_blocklist import TokenBlocklist
from app.models.user_details import Gender, UserDetails
from app.schemas.password_schema import PasswordValidationSchema
from app.utils.email import send_verification_email
from app.utils.username import generate_username


def signup_service(email, password, role, **kwargs):
    if Account.query.filter_by(email=email).first():
        return {"msg": "Email already exists"}, 400

    try:
        PasswordValidationSchema().load({"password": password})
    except ValidationError as err:
        return {"msg": "Invalid password", "errors": err.messages}, 400

    try:
        role_enum = Role[role.upper()]
    except KeyError:
        return {"msg": "Invalid role"}, 400

    if role_enum == Role.ADMIN:
        return {"msg": "Only admins can create admin accounts"}, 403

    if role_enum == Role.USER:
        required_fields = ["name", "last_name", "day", "month", "year"]
    elif role_enum == Role.ORGANIZATION:
        required_fields = ["name"]
    else:
        return {"msg": "Invalid role"}, 400

    missing_fields = [field for field in required_fields if field not in kwargs]
    if missing_fields:
        return {"msg": "Missing required fields", "missing": missing_fields}, 400

    username = kwargs.get("username") or generate_username(kwargs.get("name", email))
    verification_code = ''.join(choice(string.digits) for _ in range(6))
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=10)

    account = Account(
        email=email,
        username=username,
        role=role_enum,
        is_email_verified=False,
        verification_code=verification_code,
        verification_code_expiry=expiry_time,
    )
    account.set_password(password)
    db.session.add(account)
    db.session.flush()

    if role_enum == Role.USER:
        try:
            date_of_birth = datetime(
                int(kwargs["year"]), int(kwargs["month"]), int(kwargs["day"])
            ).date()
        except (KeyError, ValueError):
            return {"msg": "Invalid date of birth"}, 400

        user_details = UserDetails(
            account_id=account.id,
            first_name=kwargs["name"],
            last_name=kwargs["last_name"],
            phone_number=kwargs.get("phone_number"),
            gender=(
                Gender[kwargs["gender"].upper()]
                if kwargs.get("gender")
                else None
            ),
            date_of_birth=date_of_birth,
        )
        db.session.add(user_details)

    elif role_enum == Role.ORGANIZATION:
        org_details = OrganizationDetails(
            account_id=account.id,
            name=kwargs["name"],
            description=kwargs.get("description"),
            phone=kwargs.get("phone"),
        )
        db.session.add(org_details)

    db.session.commit()

    send_verification_email(email, verification_code)

    return {
        "msg": f"{account.role.value.capitalize()} created, check email for verification",
        "username": username,
    }, 201

def create_admin_account_service(current_user_id, data):
    current_account = Account.query.get(current_user_id)
    if not current_account:
        return {"msg": "User not found"}, 404

    if current_account.role != Role.ADMIN:
        return {"msg": "Only an admin can create admin accounts"}, 403

    admin_details = AdminDetails.query.filter_by(account_id=current_user_id).first()
    if not admin_details:
        return {"msg": "Admin details not found"}, 404

    if admin_details.role_level != AdminRoleLevel.SUPERADMIN:
        return {"msg": "Only a super admin can create admin accounts"}, 403

    required_fields = ["email", "password", "name", "role_level"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {"msg": f"Missing fields: {', '.join(missing_fields)}"}, 400

    try:
        role_level_enum = AdminRoleLevel(data["role_level"])
    except ValueError:
        allowed = [r.value for r in AdminRoleLevel]
        return {"msg": f"Invalid role_level. Allowed values: {', '.join(allowed)}"}, 400

    if Account.query.filter_by(email=data["email"]).first():
        return {"msg": "Email already exists"}, 400

    try:
        PasswordValidationSchema().load({"password": data["password"]})
    except ValidationError as err:
        return {"msg": "Invalid password", "errors": err.messages}, 400

    username = data.get("username") or generate_username(data["name"])
    verification_code = ''.join(choice(string.digits) for _ in range(6))
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=10)

    account = Account(
        email=data["email"],
        username=username,
        role=Role.ADMIN,
        is_email_verified=True,
        verification_code=verification_code,
        verification_code_expiry=expiry_time,
    )
    account.set_password(data["password"])
    db.session.add(account)
    db.session.flush()

    admin_details = AdminDetails(
        account_id=account.id,
        name=data["name"],
        role_level=role_level_enum,
    )
    db.session.add(admin_details)

    db.session.commit()

    return {
        "msg": "Admin account created successfully. The account has been verified by the admin.",
        "username": username,
    }, 201


def login_service(email, password):
    if not email or not password:
        return {"error": "Email and password are required"}, 400

    account = Account.query.filter(
        or_(Account.email == email, Account.username == email)
    ).first()
    if not account or not checkpw(
        password.encode("utf-8"), account.password.encode("utf-8")
    ):
        return {"msg": "Invalid credentials"}, 401

    if not account.is_email_verified:
        return {
            "msg": "Email not verified, please check your email for the verification code"
        }, 403

    account.last_login = datetime.utcnow()
    db.session.commit()

    token = create_access_token(
    identity=str(account.id),
    additional_claims={"role": account.role.value}
 )   
    return {"token": token, "role": account.role.value}, 200


def verify_service(email, code):
    if not code or not email:
        return {"msg": "Missing email or verification code"}, 400

    account = Account.query.filter_by(
        email=email, verification_code=code
    ).first()
    if not account:
        return {"msg": "Invalid email or code"}, 400

    if (
        account.verification_code_expiry
        and account.verification_code_expiry.replace(tzinfo=timezone.utc)
        < datetime.now(timezone.utc)
    ):
        return {"msg": "Verification code has expired"}, 400

    account.is_email_verified = True
    account.verification_code = None
    account.verification_code_expiry = None
    db.session.commit()

    token = create_access_token(
        identity=str(account.id),
        additional_claims={"role": account.role.value}
    )
    return {
        "msg": "Email verified",
        "token": token,
        "role": account.role.value,
    }, 200


def resend_code_service(email):
    if not email:
        return {"msg": "Email is required"}, 400

    account = Account.query.filter_by(email=email).first()
    if not account:
        return {"msg": "Account not found"}, 404

    if account.is_email_verified:
        return {"msg": "Email already verified"}, 400

    verification_code = ''.join(choice(string.digits) for _ in range(6))
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=10)

    account.verification_code = verification_code
    account.verification_code_expiry = expiry_time
    db.session.commit()

    send_verification_email(email, verification_code)
    return {"msg": "Verification code resent to your email"}, 200


def reset_password_request_service(email):
    account = Account.query.filter_by(email=email).first()
    if not account:
        return {"msg": "Email not found"}, 404

    reset_code = "".join(random.choices(string.digits, k=6))
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=10)
    account.verification_code = reset_code
    account.verification_code_expiry = expiry_time
    db.session.commit()

    send_verification_email(email, reset_code)
    return {"msg": "Reset code sent to your email"}, 200


def reset_password_service(code, new_password):
    if not code or not new_password:
        return {"msg": "Missing code or new password"}, 400

    account = Account.query.filter_by(verification_code=code).first()
    if not account:
        return {"msg": "Invalid reset code"}, 400

    try:
        PasswordValidationSchema().load({"password": new_password})
    except ValidationError as err:
        return {"msg": "Invalid password", "errors": err.messages}, 400

    account.set_password(new_password)
    account.verification_code = None
    account.verification_code_expiry = None
    db.session.commit()
    return {"msg": "Password reset successfully"}, 200


def logout_service():
    try:
        jwt_data = get_jwt()
        jti = jwt_data.get("jti")
        if not jti:
            return {"msg": "Invalid token: missing jti"}, 400

        existing_token = TokenBlocklist.query.filter_by(jti=jti).first()
        if existing_token:
            return {"msg": "Token already revoked"}, 400

        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()

        return {"msg": "Logout successful"}, 200
    except Exception as e:
        db.session.rollback()
        return {"msg": "An error occurred", "error": str(e)}, 500

