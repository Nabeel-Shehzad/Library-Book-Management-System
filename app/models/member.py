from app import db
from datetime import datetime

class Member(db.Model):
    """Member model for storing library member information."""
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship with loans
    loans = db.relationship('Loan', backref='member', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Member {self.name} ({self.email})>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_active_loans(self):
        """Get all active loans for this member."""
        return [loan for loan in self.loans if loan.status == 'active']
