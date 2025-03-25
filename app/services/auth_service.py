from ..extensions import db, jwt
from ..models.user import User
from ..utils.username import generate_username
from ..utils.email import send_verification_email
from flask_jwt_extended import create_access_token, get_jwt_identity
from bcrypt import checkpw, hashpw, gensalt
import random
import string

def signup_service(name, email, password):
    if User.query.filter_by(email=email).first():
        return {"msg": "Email already exists"}, 400

    username = generate_username(name)
    verification_code = ''.join(random.choices(string.digits, k=6))
    
    user = User(name=name, email=email, username=username, verification_code=verification_code)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    send_verification_email(email, verification_code)
    return {"msg": "User created, check email for verification", "username": username}, 201

def login_service(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return {"msg": "Invalid credentials"}, 401

    if not user.is_verified:
        return {"msg": "Email not verified"}, 403

    token = create_access_token(identity=user.id)
    return {"token": token}, 200

def verify_service(code):
    if not code:
        return {"msg": "Missing verification code"}, 400
    
    user = User.query.filter_by(verification_code=code).first()
    if user:
        user.is_verified = True
        user.verification_code = None
        db.session.commit()
        token = create_access_token(identity=user.id)
        return {"msg": "Email verified", "token": token}, 200
    return {"msg": "Invalid verification code"}, 400

def reset_password_request_service(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"msg": "Email not found"}, 404

    reset_code = ''.join(random.choices(string.digits, k=6))
    user.verification_code = reset_code
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