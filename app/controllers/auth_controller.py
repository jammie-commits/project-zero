from flask import request, Blueprint
from flask_restful import Resource, Api
from app.models.member import Member
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)
auth_api = Api(auth_bp)

class AuthResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Fetch member by email
        member = Member.query.filter_by(email=email).first()

        if member and member.check_password(password):
            # Allow both Admin and Supervisor roles for authentication
            if member.role in ['admin', 'supervisor']:
                # Generate JWT token with user's role and id
                access_token = create_access_token(identity={"id": member.id, "role": member.role})
                return {"access_token": access_token}, 200

        return {"error": "Invalid credentials or access denied"}, 401

# Add the resource to the API
auth_api.add_resource(AuthResource, '/login')