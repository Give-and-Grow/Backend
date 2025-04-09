import datetime
from ..extensions import db, jwt
from ..models.user import User
from ..models.token_blocklist import TokenBlocklist
from ..utils.username import generate_username
from ..utils.email import send_verification_email
from sqlalchemy import or_
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from bcrypt import checkpw, hashpw, gensalt
from datetime import datetime, timedelta, timezone

import random
import string

def signup_service(name, email, password, last_name, day, month, year, gender, phone_number):
    if User.query.filter_by(email=email).first():
        return {"msg": "Email already exists"}, 400

    username = generate_username(name)
    verification_code = ''.join(random.choices(string.digits, k=6))
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=10)

    try:
        date_of_birth = datetime(int(year), int(month), int(day)).date()
    except ValueError:
        return {"msg": "Invalid date of birth"}, 400

    user = User(
        name=name,
        last_name=last_name,
        email=email,
        username=username,
        gender=gender,
        phone_number=phone_number,
        date_of_birth=date_of_birth,
        verification_code=verification_code,
        verification_code_expiry=expiry_time
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    send_verification_email(email, verification_code)
    return {"msg": "User created, check email for verification", "username": username}, 201


def login_service(identifier, password):
    if not identifier or not password:
        return {'error': 'Email and password are required'}, 200
    
    user = User.query.filter(
        or_(User.username == identifier, User.email == identifier)
    ).first()

    if not user or not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return {"msg": "Invalid credentials"}, 401

    if not user.is_verified:
        return {"msg": "Email not verified"}, 403

    token = create_access_token(identity=str(user.id))  
    return {"token": token}, 200

def logout_service():
    try:
        
        jwt_data = get_jwt()
        jti = jwt_data.get('jti')  
        if not jti:
            return {"msg": "Invalid token: missing jti"}, 400

      
        identity = get_jwt_identity()  

  
        existing_token = TokenBlocklist.query.filter_by(jti=jti).first()
        if existing_token:
            return {"msg": "Token already revoked. You are already logged out."}, 400

        now = datetime.now(timezone.utc)  
        db.session.add(TokenBlocklist(jti=jti, created_at=now))

        db.session.commit()

        return {
            "message": "Logout successful!",
            "user_id": identity, 
            "revoked_token": jti 
        }, 200

    except KeyError as e:
        return {"msg": f"Invalid token structure: missing {str(e)}"}, 400

    except db.exc.SQLAlchemyError as e:
        db.session.rollback()  
        return {"msg": "Database error during logout", "error": str(e)}, 500

    except Exception as e:
        return {"msg": "An unexpected error occurred", "error": str(e)}, 500

def verify_service(email, code):
    if not code or not email:
        return {"msg": "Missing email or verification code"}, 400

    user = User.query.filter_by(email=email, verification_code=code).first()

    if not user:
        return {"msg": "Invalid email or code"}, 400

    
    # if user.verification_code_expiry and user.verification_code_expiry < datetime.now(timezone.utc):    
    #     return {"msg": "Verification code has expired"}, 400

    user.is_verified = True
    user.verification_code = None
    user.verification_code_expiry = None
    db.session.commit()

    token = create_access_token(identity=user.id)
    return {"msg": "Email verified", "token": token}, 200

def resend_code_service(email):
    if not email:
        return {"msg": "Email is required"}, 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"msg": "User not found"}, 404

    if user.is_verified:
        return {"msg": "Email already verified"}, 400

    verification_code = ''.join(random.choices(string.digits, k=6))
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=10)

    user.verification_code = verification_code
    user.verification_code_expiry = expiry_time
    db.session.commit()

    send_verification_email(email, verification_code)
    return {"msg": "Verification code resent to your email"}, 200



def reset_password_request_service(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"msg": "Email not found"}, 404

    reset_code = ''.join(random.choices(string.digits, k=6))
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=10)
    user.verification_code = reset_code
    user.verification_code_expiry = expiry_time
    db.session.commit()

    send_verification_email(email, reset_code)
    return {"msg": "Reset code sent to your email"}, 200

def reset_password_service(code, new_password):
    if not code or not new_password:
        return {"msg": "Missing code or new password"}, 400

    user = User.query.filter_by(verification_code=code).first()
    if not user:
        return {"msg": "Invalid reset code"}, 400

    user.set_password(new_password)
    user.verification_code = None
    db.session.commit()
    return {"msg": "Password reset successfully"}, 200

def get_users_by_year_service(year):
    users = User.query.filter(db.extract('year', User.date_of_birth) == year).all()

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "last_name": user.last_name,
            "email": user.email,
            "date_of_birth": user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else None,
            "gender": user.gender,
            "phone_number": user.phone_number
        })

    return result