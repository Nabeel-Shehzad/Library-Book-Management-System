import pytest
import json
from app import create_app, db
from app.models import Book, Member, Loan

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def sample_book_data():
    """Sample book data for testing."""
    return {
        'title': 'Test Book',
        'author': 'Test Author',
        'isbn': '1234567890'
    }

class TestBookAPI:
    """Test cases for Book API endpoints."""
    
    def test_create_book(self, client, sample_book_data):
        """Test creating a new book."""
        response = client.post('/books', 
                             data=json.dumps(sample_book_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == sample_book_data['title']
        assert data['author'] == sample_book_data['author']
        assert data['available'] == True
    
    def test_get_all_books(self, client, sample_book_data):
        """Test getting all books."""
        # Create a book first
        client.post('/books', 
                   data=json.dumps(sample_book_data),
                   content_type='application/json')
        
        response = client.get('/books')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) >= 1
    
    def test_get_book_by_id(self, client, sample_book_data):
        """Test getting a book by ID."""
        # Create a book first
        create_response = client.post('/books', 
                                    data=json.dumps(sample_book_data),
                                    content_type='application/json')
        book_id = json.loads(create_response.data)['id']
        
        response = client.get(f'/books/{book_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == book_id
    
    def test_update_book(self, client, sample_book_data):
        """Test updating a book."""
        # Create a book first
        create_response = client.post('/books', 
                                    data=json.dumps(sample_book_data),
                                    content_type='application/json')
        book_id = json.loads(create_response.data)['id']
        
        update_data = {'title': 'Updated Title'}
        response = client.put(f'/books/{book_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Updated Title'
    
    def test_delete_book(self, client, sample_book_data):
        """Test deleting a book."""
        # Create a book first
        create_response = client.post('/books', 
                                    data=json.dumps(sample_book_data),
                                    content_type='application/json')
        book_id = json.loads(create_response.data)['id']
        
        response = client.delete(f'/books/{book_id}')
        assert response.status_code == 200
        
        # Verify book is deleted
        get_response = client.get(f'/books/{book_id}')
        assert get_response.status_code == 404
    
    def test_create_book_validation_error(self, client):
        """Test creating a book with validation errors."""
        invalid_data = {'title': ''}  # Missing required fields
        response = client.post('/books', 
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
