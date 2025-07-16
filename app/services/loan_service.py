from app import db
from app.models.loan import Loan
from app.models.book import Book
from app.models.member import Member
from app.services.book_service import BookService
from app.services.member_service import MemberService
from datetime import datetime

class LoanService:
    """Service class for Loan operations."""
    
    @staticmethod
    def get_all_loans():
        """Get all loans."""
        return Loan.query.all()
    
    @staticmethod
    def get_loan_by_id(loan_id):
        """Get a loan by ID."""
        return Loan.query.get(loan_id)
    
    @staticmethod
    def get_active_loan_by_book(book_id):
        """Get active loan for a specific book."""
        return Loan.query.filter_by(book_id=book_id, status='active').first()
    
    @staticmethod
    def borrow_book(loan_data):
        """Create a new loan (borrow a book)."""
        try:
            book_id = loan_data['book_id']
            member_id = loan_data['member_id']
            
            # Validate book exists
            book = Book.query.get(book_id)
            if not book:
                return None, "Book not found"
            
            # Validate member exists
            member = Member.query.get(member_id)
            if not member:
                return None, "Member not found"
            
            # Check if book is available
            if not book.available:
                return None, "Book is not available for borrowing"
            
            # Check if there's already an active loan for this book
            existing_loan = LoanService.get_active_loan_by_book(book_id)
            if existing_loan:
                return None, "Book is already borrowed"
            
            # Create loan
            loan = Loan(
                book_id=book_id,
                member_id=member_id,
                status='active'
            )
            
            # Update book availability
            book.available = False
            
            db.session.add(loan)
            db.session.commit()
            
            return loan, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def return_book(loan_id):
        """Return a borrowed book."""
        try:
            loan = Loan.query.get(loan_id)
            if not loan:
                return None, "Loan not found"
            
            if loan.status == 'returned':
                return None, "Book has already been returned"
            
            # Update loan status
            loan.returned_at = datetime.utcnow()
            loan.status = 'returned'
            
            # Update book availability
            book = Book.query.get(loan.book_id)
            if book:
                book.available = True
            
            db.session.commit()
            
            return loan, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_member_active_loans(member_id):
        """Get all active loans for a member."""
        return Loan.query.filter_by(member_id=member_id, status='active').all()
    
    @staticmethod
    def get_book_loan_history(book_id):
        """Get loan history for a book."""
        return Loan.query.filter_by(book_id=book_id).all()
