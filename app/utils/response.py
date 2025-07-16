from flask import jsonify

class APIResponse:
    """Standardized API response helper."""
    
    @staticmethod
    def success(data=None, message="Success", status_code=200):
        """Create a success response."""
        response = {
            'success': True,
            'message': message
        }
        if data is not None:
            response['data'] = data
        
        return jsonify(response), status_code
    
    @staticmethod
    def error(message="An error occurred", status_code=400, errors=None):
        """Create an error response."""
        response = {
            'success': False,
            'message': message
        }
        if errors:
            response['errors'] = errors
        
        return jsonify(response), status_code
    
    @staticmethod
    def not_found(resource="Resource"):
        """Create a not found response."""
        return APIResponse.error(f"{resource} not found", 404)
    
    @staticmethod
    def validation_error(errors):
        """Create a validation error response."""
        return APIResponse.error("Validation error", 422, errors)
    
    @staticmethod
    def conflict(message):
        """Create a conflict response."""
        return APIResponse.error(message, 409)
