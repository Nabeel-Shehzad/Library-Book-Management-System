from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.loan_service import LoanService
from app.schemas.loan_schemas import (
    loan_schema, loan_create_schema, loan_response_schema
)
from marshmallow import ValidationError

# Create namespace for API documentation
loans_ns = Namespace('loans', description='Loan management operations')

# Define API models for documentation
loan_create_model = loans_ns.model('LoanCreate', {
    'book_id': fields.Integer(required=True, description='Book ID to borrow'),
    'member_id': fields.Integer(required=True, description='Member ID who is borrowing')
})

loan_response_model = loans_ns.model('LoanResponse', {
    'loan_id': fields.Integer(description='Loan ID'),
    'book_id': fields.Integer(description='Book ID'),
    'member_id': fields.Integer(description='Member ID'),
    'borrowed_at': fields.DateTime(description='Borrowed timestamp'),
    'status': fields.String(description='Loan status'),
    'message': fields.String(description='Response message')
})

@loans_ns.route('')
class LoanAPI(Resource):
    @loans_ns.doc('get_loans')
    def get(self):
        """Get all loans"""
        try:
            loans = LoanService.get_all_loans()
            return loan_schema.dump(loans, many=True), 200
        except Exception as e:
            return {'message': str(e)}, 500
    
    @loans_ns.doc('borrow_book')
    @loans_ns.expect(loan_create_model)
    @loans_ns.marshal_with(loan_response_model, code=201)
    def post(self):
        """Borrow a book"""
        try:
            # Validate input data
            loan_data = loan_create_schema.load(request.json)
            
            # Create loan
            loan, error = LoanService.borrow_book(loan_data)
            
            if error:
                if error in ["Book not found", "Member not found"]:
                    return {'message': error}, 404
                if error in ["Book is not available for borrowing", "Book is already borrowed"]:
                    return {'message': error}, 409
                return {'message': error}, 400
            
            response_data = {
                'loan_id': loan.id,
                'book_id': loan.book_id,
                'member_id': loan.member_id,
                'borrowed_at': loan.borrowed_at.isoformat(),
                'status': loan.status,
                'message': 'Book borrowed successfully'
            }
            
            return response_data, 201
            
        except ValidationError as e:
            return {'message': 'Validation error', 'errors': e.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500
