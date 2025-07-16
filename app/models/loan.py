from app import db
from datetime import datetime

class Loan(db.Model):
    """Loan model for storing book borrowing information."""
    __tablename__ = 'loans'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    returned_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='active', nullable=False)  # 'active' or 'returned'
    
    def __repr__(self):
        return f'<Loan Book#{self.book_id} Member#{self.member_id} Status:{self.status}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'book_id': self.book_id,
            'member_id': self.member_id,
            'borrowed_at': self.borrowed_at.isoformat() if self.borrowed_at else None,
            'returned_at': self.returned_at.isoformat() if self.returned_at else None,
            'status': self.status
        }
    
    def return_book(self):
        """Mark book as returned."""
        self.returned_at = datetime.utcnow()
        self.status = 'returned'
        # Update book availability
        if self.book:
            self.book.available = True
