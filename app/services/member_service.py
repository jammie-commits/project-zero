from app.models.member import Member
from app.repositories.member_repository import MemberRepository
from werkzeug.exceptions import BadRequest

class MemberService:
    @staticmethod
    def create_member(name, phone, email, password, role='member'):
        """ Create a new member with validation and logic for assigning roles """
        # Check if the email or phone already exists
        if Member.query.filter_by(phone=phone).first():
            raise BadRequest("Phone number already exists")
        if Member.query.filter_by(email=email).first():
            raise BadRequest("Email already exists")

        # Create new member
        new_member = Member(name=name, phone=phone, email=email, role=role)
        new_member.set_password(password)
        
        # Save the new member to the database
        MemberRepository.save(new_member)
        return new_member

    @staticmethod
    def update_member(member, name=None, phone=None, email=None):
        """ Update member's information """
        if name:
            member.name = name
        if phone:
            # Check if the phone number already exists
            if Member.query.filter_by(phone=phone).first():
                raise BadRequest("Phone number already exists")
            member.phone = phone
        if email:
            # Check if the email already exists
            if Member.query.filter_by(email=email).first():
                raise BadRequest("Email already exists")
            member.email = email

        # Save updated member to the database
        MemberRepository.save(member)
        return member

    @staticmethod
    def soft_delete_member(member):
        """ Soft delete a member by setting is_active=False """
        if not member.is_active:
            raise BadRequest("Member is already soft-deleted")
        
        member.is_active = False
        # Save the updated member
        MemberRepository.save(member)
        return member

    @staticmethod
    def restore_member(member):
        """ Restore a soft-deleted member """
        if member.is_active:
            raise BadRequest("Member is already active")

        member.is_active = True
        # Save the restored member
        MemberRepository.save(member)
        return member

    @staticmethod
    def change_role(member, new_role):
        """ Change a member's role """
        if new_role not in Member.get_all_roles():
            raise BadRequest("Invalid role")

        # Update the role
        member.role = new_role
        MemberRepository.save(member)
        return member