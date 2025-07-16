from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.book_service import BookService
from app.schemas.book_schemas import (
    book_schema, books_schema, book_create_schema, book_update_schema
)
from marshmallow import ValidationError

# Create namespace for API documentation  
books_ns = Namespace('books', description='Book management operations')

# Define API models for documentation
book_model = books_ns.model('Book', {
    'id': fields.Integer(readonly=True, description='Book ID'),
    'title': fields.String(required=True, description='Book title'),
    'author': fields.String(required=True, description='Book author'),
    'isbn': fields.String(description='Book ISBN'),
    'available': fields.Boolean(readonly=True, description='Book availability'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
})

book_create_model = books_ns.model('BookCreate', {
    'title': fields.String(required=True, description='Book title'),
    'author': fields.String(required=True, description='Book author'),
    'isbn': fields.String(description='Book ISBN')
})

book_update_model = books_ns.model('BookUpdate', {
    'title': fields.String(description='Book title'),
    'author': fields.String(description='Book author'),
    'isbn': fields.String(description='Book ISBN')
})

@books_ns.route('')
class BookListAPI(Resource):
    @books_ns.doc('list_books')
    @books_ns.marshal_list_with(book_model)
    def get(self):
        """List all books"""
        books = BookService.get_all_books()
        # Convert SQLAlchemy objects to dictionaries
        books_data = []
        for book in books:
            books_data.append({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'isbn': book.isbn,
                'available': book.available,
                'created_at': book.created_at.isoformat() if book.created_at else None,
                'updated_at': book.updated_at.isoformat() if book.updated_at else None
            })
        return books_data
    
    @books_ns.doc('create_book')
    @books_ns.expect(book_create_model)
    @books_ns.marshal_with(book_model, code=201)
    def post(self):
        """Add a new book"""
        try:
            # Validate input data
            book_data = book_create_schema.load(request.json)
            
            # Create book
            book, error = BookService.create_book(book_data)
            
            if error:
                return {'message': error}, 400
            
            # Convert to dictionary
            result = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'isbn': book.isbn,
                'available': book.available,
                'created_at': book.created_at.isoformat() if book.created_at else None,
                'updated_at': book.updated_at.isoformat() if book.updated_at else None
            }
            return result, 201
            
        except ValidationError as e:
            return {'message': 'Validation error', 'errors': e.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500

@books_ns.route('/<int:book_id>')
@books_ns.param('book_id', 'Book identifier')
class BookAPI(Resource):
    @books_ns.doc('get_book')
    @books_ns.marshal_with(book_model)
    def get(self, book_id):
        """Get book details by ID"""
        book = BookService.get_book_by_id(book_id)
        if not book:
            return {'message': 'Book not found'}, 404
        
        result = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'available': book.available,
            'created_at': book.created_at.isoformat() if book.created_at else None,
            'updated_at': book.updated_at.isoformat() if book.updated_at else None
        }
        return result
    
    @books_ns.doc('update_book')
    @books_ns.expect(book_update_model)
    @books_ns.marshal_with(book_model)
    def put(self, book_id):
        """Update a book"""
        try:
            # Validate input data
            book_data = book_update_schema.load(request.json)
            
            # Update book
            book, error = BookService.update_book(book_id, book_data)
            
            if error:
                if error == "Book not found":
                    return {'message': error}, 404
                return {'message': error}, 400
            
            result = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'isbn': book.isbn,
                'available': book.available,
                'created_at': book.created_at.isoformat() if book.created_at else None,
                'updated_at': book.updated_at.isoformat() if book.updated_at else None
            }
            return result
            
        except ValidationError as e:
            return {'message': 'Validation error', 'errors': e.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500
    
    @books_ns.doc('delete_book')
    def delete(self, book_id):
        """Delete a book"""
        success, message = BookService.delete_book(book_id)
        
        if not success:
            if message == "Book not found":
                return {'message': message}, 404
            return {'message': message}, 400
        
        return {'message': message}, 200
