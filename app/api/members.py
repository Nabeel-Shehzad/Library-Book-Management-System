from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.member_service import MemberService
from app.schemas.member_schemas import (
    member_schema, members_schema, member_create_schema, member_update_schema
)
from marshmallow import ValidationError

# Create namespace for API documentation
members_ns = Namespace('members', description='Member management operations')

# Define API models for documentation
member_model = members_ns.model('Member', {
    'id': fields.Integer(readonly=True, description='Member ID'),
    'name': fields.String(required=True, description='Member name'),
    'email': fields.String(required=True, description='Member email'),
    'phone': fields.String(description='Member phone'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
})

member_create_model = members_ns.model('MemberCreate', {
    'name': fields.String(required=True, description='Member name'),
    'email': fields.String(required=True, description='Member email'),
    'phone': fields.String(description='Member phone')
})

member_update_model = members_ns.model('MemberUpdate', {
    'name': fields.String(description='Member name'),
    'email': fields.String(description='Member email'),
    'phone': fields.String(description='Member phone')
})

@members_ns.route('')
class MemberListAPI(Resource):
    @members_ns.doc('list_members')
    @members_ns.marshal_list_with(member_model)
    def get(self):
        """List all members"""
        members = MemberService.get_all_members()
        return members_schema.dump(members)
    
    @members_ns.doc('create_member')
    @members_ns.expect(member_create_model)
    @members_ns.marshal_with(member_model, code=201)
    def post(self):
        """Register a new member"""
        try:
            # Validate input data
            member_data = member_create_schema.load(request.json)
            
            # Create member
            member, error = MemberService.create_member(member_data)
            
            if error:
                if error == "Email already exists":
                    return {'message': error}, 409
                return {'message': error}, 400
            
            return member_schema.dump(member), 201
            
        except ValidationError as e:
            return {'message': 'Validation error', 'errors': e.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500

@members_ns.route('/<int:member_id>')
@members_ns.param('member_id', 'Member identifier')
class MemberAPI(Resource):
    @members_ns.doc('get_member')
    @members_ns.marshal_with(member_model)
    def get(self, member_id):
        """Get member details by ID"""
        member = MemberService.get_member_by_id(member_id)
        if not member:
            return {'message': 'Member not found'}, 404
        
        return member_schema.dump(member)
    
    @members_ns.doc('update_member')
    @members_ns.expect(member_update_model)
    @members_ns.marshal_with(member_model)
    def put(self, member_id):
        """Update a member"""
        try:
            # Validate input data
            member_data = member_update_schema.load(request.json)
            
            # Update member
            member, error = MemberService.update_member(member_id, member_data)
            
            if error:
                if error == "Member not found":
                    return {'message': error}, 404
                if error == "Email already exists":
                    return {'message': error}, 409
                return {'message': error}, 400
            
            return member_schema.dump(member)
            
        except ValidationError as e:
            return {'message': 'Validation error', 'errors': e.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500
