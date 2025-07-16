from marshmallow import Schema, fields, validate, post_load

class BookSchema(Schema):
    """Schema for Book serialization/deserialization."""
    
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    isbn = fields.Str(validate=validate.Length(max=20))
    available = fields.Bool(dump_only=True)  # Read-only field
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class BookCreateSchema(Schema):
    """Schema for creating a new book."""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    isbn = fields.Str(validate=validate.Length(max=20))

class BookUpdateSchema(Schema):
    """Schema for updating a book."""
    title = fields.Str(validate=validate.Length(min=1, max=200))
    author = fields.Str(validate=validate.Length(min=1, max=100))
    isbn = fields.Str(validate=validate.Length(max=20))

class BookListSchema(Schema):
    """Schema for listing books with pagination info."""
    books = fields.List(fields.Nested(BookSchema))
    total = fields.Int()
    page = fields.Int()
    per_page = fields.Int()

# Initialize schemas
book_schema = BookSchema()
books_schema = BookSchema(many=True)
book_create_schema = BookCreateSchema()
book_update_schema = BookUpdateSchema()
book_list_schema = BookListSchema()
