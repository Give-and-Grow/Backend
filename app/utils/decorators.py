#Backend/app/utils/decorators.py
from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt,get_jwt_identity



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

def account_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") not in ["user", "organization"]:
            return jsonify({"msg": "Users and Organizations only!"}), 403
        g.user_id = get_jwt_identity()  # ← هون نضيف الـ ID للـ g
        return fn(*args, **kwargs)
    return wrapper