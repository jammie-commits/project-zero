from flask import Blueprint
from flask_restful import Api
from app.controllers.auth_controller import AuthResource

# Define a Blueprint for authentication
auth_bp = Blueprint('auth_bp', __name__)
auth_api = Api(auth_bp)

# Register the auth resource
auth_api.add_resource(AuthResource, '/login')
