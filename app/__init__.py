from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
restx_api = Api()  # Renamed to avoid conflict with app.api module
cors = CORS()

def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    
    # Register web routes blueprint FIRST (before API)
    from app.routes import main
    app.register_blueprint(main)
    
    # Initialize API with documentation (no prefix, but move docs)
    restx_api.init_app(app, 
                 title='Library Book Management System API',
                 version='1.0',
                 description='A RESTful API for managing library books, members, and loans',
                 doc='/api-docs/'  # Move API docs to /api-docs/ instead of root
                )
    
    # Register namespaces after API is initialized
    from app.api import books, members, loans, returns
    
    restx_api.add_namespace(books.books_ns, path='/api/v1/books')
    restx_api.add_namespace(members.members_ns, path='/api/v1/members')
    restx_api.add_namespace(loans.loans_ns, path='/api/v1/loans')
    restx_api.add_namespace(returns.returns_ns, path='/api/v1/returns')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Library API is running'}, 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
