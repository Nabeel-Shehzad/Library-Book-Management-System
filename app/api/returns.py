from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.loan_service import LoanService
from app.schemas.loan_schemas import (
    loan_return_schema, loan_response_schema
)
from marshmallow import ValidationError

# Create namespace for API documentation
returns_ns = Namespace('returns', description='Book return operations')

# Define API models for documentation
return_model = returns_ns.model('BookReturn', {
    'loan_id': fields.Integer(required=True, description='Loan ID to return')
})

return_response_model = returns_ns.model('ReturnResponse', {
    'loan_id': fields.Integer(description='Loan ID'),
    'book_id': fields.Integer(description='Book ID'),
    'member_id': fields.Integer(description='Member ID'),
    'borrowed_at': fields.DateTime(description='Borrowed timestamp'),
    'returned_at': fields.DateTime(description='Returned timestamp'),
    'status': fields.String(description='Loan status'),
    'message': fields.String(description='Response message')
})

@returns_ns.route('')
class ReturnAPI(Resource):
    @returns_ns.doc('return_book')
    @returns_ns.expect(return_model)
    @returns_ns.marshal_with(return_response_model, code=200)
    def post(self):
        """Return a borrowed book"""
        try:
            # Validate input data
            return_data = loan_return_schema.load(request.json)
            loan_id = return_data['loan_id']
            
            # Return book
            loan, error = LoanService.return_book(loan_id)
            
            if error:
                if error == "Loan not found":
                    return {'message': error}, 404
                if error == "Book has already been returned":
                    return {'message': error}, 409
                return {'message': error}, 400
            
            response_data = {
                'loan_id': loan.id,
                'book_id': loan.book_id,
                'member_id': loan.member_id,
                'borrowed_at': loan.borrowed_at.isoformat(),
                'returned_at': loan.returned_at.isoformat() if loan.returned_at else None,
                'status': loan.status,
                'message': 'Book returned successfully'
            }
            
            return response_data, 200
            
        except ValidationError as e:
            return {'message': 'Validation error', 'errors': e.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500
