from app import db
from app.models.book import Book
from sqlalchemy.exc import IntegrityError

class BookService:
    """Service class for Book operations."""
    
    @staticmethod
    def get_all_books():
        """Get all books."""
        return Book.query.all()
    
    @staticmethod
    def get_book_by_id(book_id):
        """Get a book by ID."""
        return Book.query.get(book_id)
    
    @staticmethod
    def create_book(book_data):
        """Create a new book."""
        try:
            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                isbn=book_data.get('isbn')
            )
            db.session.add(book)
            db.session.commit()
            return book, None
        except IntegrityError as e:
            db.session.rollback()
            if 'isbn' in str(e):
                return None, "ISBN already exists"
            return None, "Database error occurred"
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_book(book_id, book_data):
        """Update a book."""
        try:
            book = Book.query.get(book_id)
            if not book:
                return None, "Book not found"
            
            # Update fields if provided
            if 'title' in book_data:
                book.title = book_data['title']
            if 'author' in book_data:
                book.author = book_data['author']
            if 'isbn' in book_data:
                book.isbn = book_data['isbn']
            
            db.session.commit()
            return book, None
        except IntegrityError as e:
            db.session.rollback()
            if 'isbn' in str(e):
                return None, "ISBN already exists"
            return None, "Database error occurred"
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_book(book_id):
        """Delete a book."""
        try:
            book = Book.query.get(book_id)
            if not book:
                return False, "Book not found"
            
            # Check if book has active loans
            active_loans = [loan for loan in book.loans if loan.status == 'active']
            if active_loans:
                return False, "Cannot delete book with active loans"
            
            db.session.delete(book)
            db.session.commit()
            return True, "Book deleted successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def is_book_available(book_id):
        """Check if a book is available for borrowing."""
        book = Book.query.get(book_id)
        return book and book.available
    
    @staticmethod
    def set_book_availability(book_id, available):
        """Set book availability status."""
        try:
            book = Book.query.get(book_id)
            if not book:
                return False, "Book not found"
            
            book.available = available
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
