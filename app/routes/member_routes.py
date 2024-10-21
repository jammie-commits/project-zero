from flask import Blueprint
from flask_restful import Api
from app.controllers.member_controller import (
    MemberListResource,
    MemberResource,
    InactiveMemberResource,
    RestoreMemberResource,
    ChangeRoleResource,
    SoftDeleteMemberResource,
    CreateMemberResource
)

# Define a Blueprint for members
member_bp = Blueprint('member_bp', __name__)
member_api = Api(member_bp)

# Register the member resources
member_api.add_resource(MemberListResource, '/')
member_api.add_resource(MemberResource, '/<int:id>')
member_api.add_resource(InactiveMemberResource, '/inactive')
member_api.add_resource(RestoreMemberResource, '/<int:id>/restore')
member_api.add_resource(ChangeRoleResource, '/<int:id>/role')
member_api.add_resource(CreateMemberResource, '/')
member_api.add_resource(SoftDeleteMemberResource, '/<int:id>/delete')
