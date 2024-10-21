from app import db
from app.models.member import Member

class MemberRepository:
    @staticmethod
    def create_member(data):
        """Create a new member"""
        new_member = Member(
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            role=data.get('role', 'member'),  # Default to 'member' if not provided
            is_active=True
        )
        new_member.set_password(data['password'])
        db.session.add(new_member)
        db.session.commit()
        return new_member

    @staticmethod
    def get_member_by_id(member_id):
        """Fetch a member by their ID"""
        return Member.query.get(member_id)

    @staticmethod
    def update_member(member_id, data):
        """Update a member's non-sensitive information"""
        member = Member.query.get(member_id)
        if member:
            # Update only non-sensitive fields (name, phone, email)
            if 'name' in data:
                member.name = data['name']
            if 'phone' in data:
                member.phone = data['phone']
            if 'email' in data:
                member.email = data['email']
            db.session.commit()
            return member
        return None

    @staticmethod
    def soft_delete_member(member_id):
        """Soft delete a member by setting is_active to False"""
        member = Member.query.get(member_id)
        if member:
            member.is_active = False
            db.session.commit()
            return member
        return None

    @staticmethod
    def restore_member(member_id):
        """Restore a soft-deleted member by setting is_active to True"""
        member = Member.query.get(member_id)
        if member:
            member.is_active = True
            db.session.commit()
            return member
        return None

    @staticmethod
    def update_role(member_id, new_role):
        """Update a member's role"""
        member = Member.query.get(member_id)
        if member and new_role in Member.get_all_roles():
            member.role = new_role
            db.session.commit()
            return member
        return None

    @staticmethod
    def get_all_active_members():
        """Fetch all active members"""
        return Member.query.filter_by(is_active=True).all()

    @staticmethod
    def get_all_inactive_members():
        """Fetch all inactive (soft-deleted) members"""
        return Member.query.filter_by(is_active=False).all()

    @staticmethod
    def get_member_by_email(email):
        """Fetch a member by their email"""
        return Member.query.filter_by(email=email).first()