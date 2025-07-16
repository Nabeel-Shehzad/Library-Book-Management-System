from app import db
from app.models.member import Member
from sqlalchemy.exc import IntegrityError

class MemberService:
    """Service class for Member operations."""
    
    @staticmethod
    def get_all_members():
        """Get all members."""
        return Member.query.all()
    
    @staticmethod
    def get_member_by_id(member_id):
        """Get a member by ID."""
        return Member.query.get(member_id)
    
    @staticmethod
    def get_member_by_email(email):
        """Get a member by email."""
        return Member.query.filter_by(email=email).first()
    
    @staticmethod
    def create_member(member_data):
        """Create a new member."""
        try:
            # Check if email already exists
            existing_member = MemberService.get_member_by_email(member_data['email'])
            if existing_member:
                return None, "Email already exists"
            
            member = Member(
                name=member_data['name'],
                email=member_data['email'],
                phone=member_data.get('phone')
            )
            db.session.add(member)
            db.session.commit()
            return member, None
        except IntegrityError as e:
            db.session.rollback()
            if 'email' in str(e):
                return None, "Email already exists"
            return None, "Database error occurred"
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_member(member_id, member_data):
        """Update a member."""
        try:
            member = Member.query.get(member_id)
            if not member:
                return None, "Member not found"
            
            # Check if email is being updated and if it already exists
            if 'email' in member_data and member_data['email'] != member.email:
                existing_member = MemberService.get_member_by_email(member_data['email'])
                if existing_member:
                    return None, "Email already exists"
            
            # Update fields if provided
            if 'name' in member_data:
                member.name = member_data['name']
            if 'email' in member_data:
                member.email = member_data['email']
            if 'phone' in member_data:
                member.phone = member_data['phone']
            
            db.session.commit()
            return member, None
        except IntegrityError as e:
            db.session.rollback()
            if 'email' in str(e):
                return None, "Email already exists"
            return None, "Database error occurred"
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def has_active_loans(member_id):
        """Check if member has active loans."""
        member = Member.query.get(member_id)
        if not member:
            return False
        return len(member.get_active_loans()) > 0
    
    @staticmethod
    def get_member_loans(member_id):
        """Get all loans for a member."""
        member = Member.query.get(member_id)
        if not member:
            return None
        return member.loans
