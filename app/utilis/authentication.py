from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from functools import wraps

def authenticate_role(allowed_roles):
    """
    A decorator to protect routes based on the user's role.
    :param allowed_roles: List of roles that are allowed to access the route.
    """
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            current_user = get_jwt_identity()
            
            if current_user['role'] not in allowed_roles:
                return jsonify({"error": "Unauthorized"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper

def authenticate_admin():
    return authenticate_role(['admin'])

def authenticate_supervisor():
    return authenticate_role(['admin', 'supervisor'])