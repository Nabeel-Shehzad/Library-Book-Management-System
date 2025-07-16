class LibraryException(Exception):
    """Base exception for library operations."""
    pass

class BookNotAvailableException(LibraryException):
    """Raised when a book is not available for borrowing."""
    pass

class BookNotFoundException(LibraryException):
    """Raised when a book is not found."""
    pass

class MemberNotFoundException(LibraryException):
    """Raised when a member is not found."""
    pass

class LoanNotFoundException(LibraryException):
    """Raised when a loan is not found."""
    pass

class EmailAlreadyExistsException(LibraryException):
    """Raised when trying to create a member with an existing email."""
    pass

class ISBNAlreadyExistsException(LibraryException):
    """Raised when trying to create a book with an existing ISBN."""
    pass

class ActiveLoansExistException(LibraryException):
    """Raised when trying to delete a book that has active loans."""
    pass
