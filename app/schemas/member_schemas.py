from marshmallow import Schema, fields, validate

class MemberSchema(Schema):
    """Schema for Member serialization/deserialization."""
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    phone = fields.Str(validate=validate.Length(max=20))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class MemberCreateSchema(Schema):
    """Schema for creating a new member."""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    phone = fields.Str(validate=validate.Length(max=20))

class MemberUpdateSchema(Schema):
    """Schema for updating a member."""
    name = fields.Str(validate=validate.Length(min=1, max=100))
    email = fields.Email(validate=validate.Length(max=120))
    phone = fields.Str(validate=validate.Length(max=20))

class MemberListSchema(Schema):
    """Schema for listing members."""
    members = fields.List(fields.Nested(MemberSchema))
    total = fields.Int()

# Initialize schemas
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
member_create_schema = MemberCreateSchema()
member_update_schema = MemberUpdateSchema()
member_list_schema = MemberListSchema()
