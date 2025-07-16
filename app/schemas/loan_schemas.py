from marshmallow import Schema, fields, validate

class LoanSchema(Schema):
    """Schema for Loan serialization/deserialization."""
    
    id = fields.Int(dump_only=True)
    book_id = fields.Int(required=True)
    member_id = fields.Int(required=True)
    borrowed_at = fields.DateTime(dump_only=True)
    returned_at = fields.DateTime(dump_only=True)
    status = fields.Str(dump_only=True)

class LoanCreateSchema(Schema):
    """Schema for creating a new loan (borrowing a book)."""
    book_id = fields.Int(required=True)
    member_id = fields.Int(required=True)

class LoanReturnSchema(Schema):
    """Schema for returning a book."""
    loan_id = fields.Int(required=True)

class LoanResponseSchema(Schema):
    """Schema for loan response."""
    loan_id = fields.Int()
    book_id = fields.Int()
    member_id = fields.Int()
    borrowed_at = fields.DateTime()
    returned_at = fields.DateTime()
    status = fields.Str()
    message = fields.Str()

# Initialize schemas
loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)
loan_create_schema = LoanCreateSchema()
loan_return_schema = LoanReturnSchema()
loan_response_schema = LoanResponseSchema()
