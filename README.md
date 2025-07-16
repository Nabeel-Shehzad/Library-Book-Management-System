# Library Book Management System

A RESTful API for managing library books, members, and loans built with Flask and SQLite.

## 🚀 Features

- **Book Management**: Add, view, update, and delete books
- **Member Management**: Register and manage library members
- **Loan System**: Borrow and return books with automatic availability tracking
- **Data Validation**: Comprehensive input validation with Marshmallow
- **API Documentation**: Auto-generated Swagger documentation
- **SQLite Database**: Lightweight, file-based database
- **RESTful Design**: Clean, resource-based API endpoints

## 📋 API Endpoints

### Books
- `GET /books` - List all books
- `POST /books` - Add new book
- `GET /books/{id}` - View book details
- `PUT /books/{id}` - Update book
- `DELETE /books/{id}` - Delete book

### Members
- `POST /members` - Register member
- `GET /members` - List all members
- `PUT /members/{id}` - Update member

### Loans
- `POST /loans` - Borrow book
- `POST /returns` - Return book

## 🛠️ Technology Stack

- **Framework**: Flask 2.3.3
- **Database**: SQLite
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Validation**: Marshmallow
- **API Documentation**: Flask-RESTX
- **Testing**: pytest

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Library Book Management System"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy .env file and update values as needed
   cp .env.example .env
   ```

5. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

## 🚀 Running the Application

1. **Start the development server**
   ```bash
   python run.py
   ```

2. **Access the application**
   - API Base URL: `http://localhost:5000`
   - API Documentation: `http://localhost:5000/docs/`

## 📖 API Usage Examples

### Create a Book
```bash
curl -X POST http://localhost:5000/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "978-0-7432-7356-5"
  }'
```

### Register a Member
```bash
curl -X POST http://localhost:5000/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "123-456-7890"
  }'
```

### Borrow a Book
```bash
curl -X POST http://localhost:5000/loans \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "member_id": 1
  }'
```

### Return a Book
```bash
curl -X POST http://localhost:5000/returns \
  -H "Content-Type: application/json" \
  -d '{
    "loan_id": 1
  }'
```

## 🗄️ Database Schema

### Books Table
- `id` (Primary Key)
- `title` (Required)
- `author` (Required)
- `isbn` (Unique, Optional)
- `available` (Boolean, Default: True)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### Members Table
- `id` (Primary Key)
- `name` (Required)
- `email` (Required, Unique)
- `phone` (Optional)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### Loans Table
- `id` (Primary Key)
- `book_id` (Foreign Key to Books)
- `member_id` (Foreign Key to Members)
- `borrowed_at` (Timestamp)
- `returned_at` (Timestamp, Nullable)
- `status` (active/returned)

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## 📚 Project Structure

```
Library Book Management System/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration settings
│   ├── models/              # SQLAlchemy models
│   ├── api/                 # API endpoints
│   ├── services/            # Business logic
│   ├── schemas/             # Marshmallow schemas
│   └── utils/               # Utility functions
├── instance/
│   └── library.db          # SQLite database
├── tests/                  # Test files
├── requirements.txt        # Dependencies
├── run.py                 # Application entry point
└── README.md
```

## 🔧 Configuration

Environment variables in `.env`:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/library.db
```

## 📊 Business Logic

### Book Borrowing Process
1. Validate book and member existence
2. Check book availability
3. Create loan record with 'active' status
4. Update book availability to False
5. Return loan confirmation

### Book Return Process
1. Validate loan existence and status
2. Update loan record with return timestamp
3. Set loan status to 'returned'
4. Update book availability to True
5. Return success confirmation

## 🚦 Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `409` - Conflict (resource already exists, book not available)
- `422` - Unprocessable Entity
- `500` - Internal Server Error

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Submit a pull request

## 📞 Support

For questions or issues, please create an issue in the GitHub repository.
