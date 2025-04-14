#backend/app/services/user_profile_services
from bcrypt import checkpw
from flask import jsonify
from werkzeug.security import check_password_hash
from marshmallow import ValidationError

from ..schemas.user_schema import UpdateProfileSchema
from ..schemas.user_schema import ChangePasswordSchema 
from ..models.user import User
from ..extensions import db
from ..utils.duration_since import get_duration_since


def get_own_profile_service(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"msg": "User not found"}, 404

    return {
        "name": user.name,
        "last_name": user.last_name,
        "email": user.email,
        "username": user.username,
        "phone_number": user.phone_number,
        "gender": user.gender,
        "date_of_birth": user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else None,
        "city": user.city,
        "village": user.village,
        "bio": user.bio,
        "profile_picture": user.profile_picture,
        "experience": user.experience,
        "is_verified": user.is_verified,
        "registration_duration": get_duration_since(user.registration_date),
        "identity_verification_status": user.identity_verification_status.value if user.identity_verification_status else None,

    }, 200

def update_profile_service(user_id, data):
    try:
        schema = UpdateProfileSchema()
        validated_data = schema.load(data)

        user = User.query.get(user_id)
        if not user:
            return {"msg": "User not found"}, 404

        new_username = validated_data.get('username')
        if new_username and new_username != user.username:
            if User.query.filter(User.username == new_username, User.id != user_id).first():
                return {"msg": f"Username '{new_username}' is already taken"}, 400
            user.username = new_username

        for field in [
           'name', 'last_name', 'phone_number', 'gender', 'city', 
           'village', 'bio', 'experience', 'date_of_birth', 'profile_picture','identity_picture'
        ]:
            if field in validated_data and getattr(user, field) != validated_data[field]:
                setattr(user, field, validated_data[field])

        db.session.commit()
        return {"msg": "Profile updated successfully"}, 200

    except ValidationError as ve:
        return {"msg": "Validation error", "errors": ve.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {"msg": "An error occurred", "error": str(e)}, 500
    
#backend/app/services/user_profile_services
def change_password_service(user_id, data):
    try:
        schema = ChangePasswordSchema(context={
            "old_password": data.get("old_password"),
            "new_password": data.get("new_password")
        })
        validated_data = schema.load(data)

        old_password = data.get("old_password")
        new_password = validated_data.get('new_password')

        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        if not checkpw(old_password.encode('utf-8'), user.password.encode('utf-8')):
            return {'message': 'Old password is incorrect'}, 400

        user.set_password(new_password)
        db.session.commit()

        return {'status': 'success', 'message': 'Password changed successfully'}, 200

    except ValidationError as ve:
        return {'message': 'Validation error', 'errors': ve.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {'message': 'An error occurred', 'error': str(e)}, 500

