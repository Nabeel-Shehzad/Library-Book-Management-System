from flask import Blueprint, render_template

# Create the main blueprint for web pages
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Dashboard page."""
    return render_template('index.html')

@main.route('/books')
def books():
    """Books management page."""
    return render_template('books.html')

@main.route('/members')
def members():
    """Members management page."""
    return render_template('members.html')

@main.route('/loans')
def loans():
    """Loans management page."""
    return render_template('loans.html')
