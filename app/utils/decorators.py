#Backend/app/utils/decorators.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != required_role:
                return jsonify({"msg": f"{required_role.capitalize()}s only!"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

admin_required = role_required("admin")
user_required = role_required("user")
organization_required = role_required("organization")
