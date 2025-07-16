# Import all schemas here for easy access
from .book_schemas import (
    book_schema, books_schema, book_create_schema, 
    book_update_schema, book_list_schema
)
from .member_schemas import (
    member_schema, members_schema, member_create_schema,
    member_update_schema, member_list_schema
)
from .loan_schemas import (
    loan_schema, loans_schema, loan_create_schema,
    loan_return_schema, loan_response_schema
)

__all__ = [
    'book_schema', 'books_schema', 'book_create_schema', 'book_update_schema', 'book_list_schema',
    'member_schema', 'members_schema', 'member_create_schema', 'member_update_schema', 'member_list_schema',
    'loan_schema', 'loans_schema', 'loan_create_schema', 'loan_return_schema', 'loan_response_schema'
]
