from flask import request, Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.member import Member
from app.repositories.member_repository import MemberRepository
from app.services.member_service import MemberService
from werkzeug.exceptions import BadRequest
from app import db

member_bp = Blueprint('member_bp', __name__)
member_api = Api(member_bp)

class MemberListResource(Resource):
    @jwt_required()
    def get(self):
        """ List all active members for Admins and Supervisors """
        current_user = get_jwt_identity()
        
        if current_user['role'] not in ['admin', 'supervisor']:
            return {"error": "Unauthorized"}, 403

        members = Member.query.filter_by(is_active=True).all()
        return [member.to_dict() for member in members], 200

class MemberResource(Resource):
    @jwt_required()
    def get(self, id):
        """ Get a single member's details by ID """
        current_user = get_jwt_identity()
        member = Member.query.get_or_404(id)

        if current_user['role'] not in ['admin', 'supervisor']:
            return {"error": "Unauthorized"}, 403

        # Allow members to only view their own details if role is supervisor or member
        if current_user['role'] == 'supervisor' and current_user['id'] != id:
            return {"error": "Unauthorized"}, 403

        return member.to_dict(), 200

    @jwt_required()
    def put(self, id):
        """ Update member's information (name, phone, email) """
        current_user = get_jwt_identity()
        member = Member.query.get_or_404(id)
        if current_user['role'] not in ['admin', 'supervisor']:
            return {"error": "Unauthorized"}, 403

        if current_user['role'] == 'supervisor':
            # If the user is a supervisor, we prevent role or password changes.
            # Sensitive information should be handled by admins only.
            data = request.get_json()
            if 'role' in data or 'password' in data:
                return {"error": "Supervisors cannot change sensitive information (role/password)"}, 403



        data = request.get_json()
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')

        if name:
            member.name = name
        if phone:
            if Member.query.filter_by(phone=phone).first():
                return {"error": "Phone number already exists"}, 400
            member.phone = phone
        if email:
            if Member.query.filter_by(email=email).first():
                return {"error": "Email already exists"}, 400
            member.email = email

        db.session.commit()
        return member.to_dict(), 200

class InactiveMemberResource(Resource):
    @jwt_required()
    def get(self):
        """ Fetch all inactive members for Admins only """
        current_user = get_jwt_identity()

        if current_user['role'] != 'admin':
            return {"error": "Unauthorized"}, 403

        inactive_members = Member.query.filter_by(is_active=False).all()
        return [member.to_dict() for member in inactive_members], 200

class RestoreMemberResource(Resource):
    @jwt_required()
    def post(self, id):
        """ Restore a soft-deleted member for Admins only """
        current_user = get_jwt_identity()

        if current_user['role'] != 'admin':
            return {"error": "Unauthorized"}, 403

        member = Member.query.get_or_404(id)

        # Check if the member is already active
        if member.is_active:
            return {"error": "Member is already active"}, 400

        # Restore the member by setting is_active to True
        member.is_active = True
        db.session.commit()
        return {"message": "Member restored successfully"}, 200

class ChangeRoleResource(Resource):
    @jwt_required()
    def put(self, id):
        """ Change a member's role for Admins only """
        current_user = get_jwt_identity()

        if current_user['role'] != 'admin':
            return {"error": "Unauthorized"}, 403

        member = Member.query.get_or_404(id)
        data = request.get_json()
        new_role = data.get('role')

        if new_role not in Member.get_all_roles():
            return {"error": "Invalid role"}, 400

        # Prevent self-role change
        if current_user['id'] == id:
            return {"error": "You cannot change your own role"}, 403

        # Change role
        if member.assign_role(new_role):
            return {"message": "Role updated successfully"}, 200
        else:
            return {"error": "Failed to update role"}, 400
class SoftDeleteMemberResource(Resource):
    @jwt_required()
    def delete(self, id):
        """ Soft delete a member (set is_active to False) """
        current_user = get_jwt_identity()

        if current_user['role'] != 'admin':
            return {"error": "Unauthorized"}, 403

        member = Member.query.get_or_404(id)

        # If the member is already inactive, return an error
        if not member.is_active:
            return {"error": "Member is already soft-deleted"}, 400

        # Soft delete the member by setting is_active to False
        member.is_active = False
        db.session.commit()
        return {"message": "Member soft-deleted successfully"}, 200


class CreateMemberResource(Resource):
    @jwt_required()
    def post(self):
        """ Create a new member for Admins only """
        current_user = get_jwt_identity()

        if current_user['role'] != 'admin':
            return {"error": "Unauthorized"}, 403

        data = request.get_json()
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'member')  # Default role is 'member'

        # Validate uniqueness of email and phone
        if Member.query.filter_by(phone=phone).first():
            return {"error": "Phone number already exists"}, 400
        if Member.query.filter_by(email=email).first():
            return {"error": "Email already exists"}, 400

        # Create a new member
        new_member = Member(name=name, phone=phone, email=email, role=role)
        new_member.set_password(password)
        db.session.add(new_member)
        db.session.commit()

        return new_member.to_dict(), 201



# Add resources to the API
member_api.add_resource(MemberListResource, '/')
member_api.add_resource(MemberResource, '/<int:id>')
member_api.add_resource(InactiveMemberResource, '/inactive')
member_api.add_resource(RestoreMemberResource, '/<int:id>/restore')
member_api.add_resource(ChangeRoleResource, '/<int:id>/role')
member_api.add_resource(CreateMemberResource, '/')
member_api.add_resource(SoftDeleteMemberResource, '/<int:id>/delete')