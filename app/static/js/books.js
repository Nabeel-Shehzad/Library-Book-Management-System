// Books management JavaScript

let booksData = [];
let filteredBooks = [];

document.addEventListener('DOMContentLoaded', function() {
    loadBooks();
    initializeEventListeners();
});

function initializeEventListeners() {
    // Search functionality
    const searchInput = document.getElementById('searchBooks');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(filterBooks, 300));
    }
    
    // Filter functionality
    const filterSelect = document.getElementById('filterAvailability');
    if (filterSelect) {
        filterSelect.addEventListener('change', filterBooks);
    }
    
    // Form submissions
    const addBookForm = document.getElementById('addBookForm');
    if (addBookForm) {
        addBookForm.addEventListener('submit', handleAddBook);
    }
    
    const editBookForm = document.getElementById('editBookForm');
    if (editBookForm) {
        editBookForm.addEventListener('submit', handleEditBook);
    }
}

async function loadBooks() {
    try {
        showLoadingState(document.getElementById('booksTableBody'));
        booksData = await API.getBooks();
        filteredBooks = [...booksData];
        renderBooksTable();
    } catch (error) {
        console.error('Error loading books:', error);
        showToast('Error loading books: ' + error.message, 'danger');
        document.getElementById('booksTableBody').innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-danger py-4">
                    <i class="fas fa-exclamation-triangle fa-2x mb-3"></i>
                    <br>Error loading books
                </td>
            </tr>
        `;
    }
}

function renderBooksTable() {
    const tbody = document.getElementById('booksTableBody');
    
    if (filteredBooks.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-muted py-4">
                    <i class="fas fa-book fa-2x mb-3"></i>
                    <br>No books found
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = filteredBooks.map(book => `
        <tr>
            <td>${book.id}</td>
            <td>
                <strong>${escapeHtml(book.title)}</strong>
            </td>
            <td>${escapeHtml(book.author)}</td>
            <td>${book.isbn || 'N/A'}</td>
            <td>
                <span class="badge ${book.available ? 'bg-success' : 'bg-warning'}">
                    <i class="fas ${book.available ? 'fa-check-circle' : 'fa-clock'} me-1"></i>
                    ${book.available ? 'Available' : 'Borrowed'}
                </span>
            </td>
            <td>${formatDate(book.created_at)}</td>
            <td>
                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-sm btn-outline-primary" onclick="editBook(${book.id})" title="Edit Book">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button type="button" class="btn btn-sm btn-outline-danger" onclick="deleteBook(${book.id})" title="Delete Book">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
    
    showLoadingState(tbody, false);
}

function filterBooks() {
    const searchTerm = document.getElementById('searchBooks').value.toLowerCase();
    const availabilityFilter = document.getElementById('filterAvailability').value;
    
    filteredBooks = booksData.filter(book => {
        const matchesSearch = !searchTerm || 
            book.title.toLowerCase().includes(searchTerm) ||
            book.author.toLowerCase().includes(searchTerm) ||
            (book.isbn && book.isbn.toLowerCase().includes(searchTerm));
        
        const matchesAvailability = !availabilityFilter || 
            book.available.toString() === availabilityFilter;
        
        return matchesSearch && matchesAvailability;
    });
    
    renderBooksTable();
}

function clearFilters() {
    document.getElementById('searchBooks').value = '';
    document.getElementById('filterAvailability').value = '';
    filteredBooks = [...booksData];
    renderBooksTable();
}

async function handleAddBook(event) {
    event.preventDefault();
    
    const form = event.target;
    if (!validateForm(form)) {
        showToast('Please fill in all required fields correctly', 'danger');
        return;
    }
    
    const bookData = {
        title: document.getElementById('bookTitle').value.trim(),
        author: document.getElementById('bookAuthor').value.trim(),
        isbn: document.getElementById('bookISBN').value.trim() || null
    };
    
    try {
        showLoadingState(form);
        const newBook = await API.createBook(bookData);
        
        // Add to local data
        booksData.push(newBook);
        filterBooks(); // Refresh the display
        
        // Close modal and reset form
        const modal = bootstrap.Modal.getInstance(document.getElementById('addBookModal'));
        modal.hide();
        clearForm(form);
        
        showToast('Book added successfully!', 'success');
        
    } catch (error) {
        console.error('Error adding book:', error);
        showToast('Error adding book: ' + error.message, 'danger');
    } finally {
        showLoadingState(form, false);
    }
}

async function editBook(bookId) {
    try {
        const book = await API.getBook(bookId);
        
        // Populate edit form
        document.getElementById('editBookId').value = book.id;
        document.getElementById('editBookTitle').value = book.title;
        document.getElementById('editBookAuthor').value = book.author;
        document.getElementById('editBookISBN').value = book.isbn || '';
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('editBookModal'));
        modal.show();
        
    } catch (error) {
        console.error('Error loading book details:', error);
        showToast('Error loading book details: ' + error.message, 'danger');
    }
}

async function handleEditBook(event) {
    event.preventDefault();
    
    const form = event.target;
    if (!validateForm(form)) {
        showToast('Please fill in all required fields correctly', 'danger');
        return;
    }
    
    const bookId = parseInt(document.getElementById('editBookId').value);
    const bookData = {
        title: document.getElementById('editBookTitle').value.trim(),
        author: document.getElementById('editBookAuthor').value.trim(),
        isbn: document.getElementById('editBookISBN').value.trim() || null
    };
    
    try {
        showLoadingState(form);
        const updatedBook = await API.updateBook(bookId, bookData);
        
        // Update local data
        const index = booksData.findIndex(book => book.id === bookId);
        if (index !== -1) {
            booksData[index] = updatedBook;
            filterBooks(); // Refresh the display
        }
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('editBookModal'));
        modal.hide();
        
        showToast('Book updated successfully!', 'success');
        
    } catch (error) {
        console.error('Error updating book:', error);
        showToast('Error updating book: ' + error.message, 'danger');
    } finally {
        showLoadingState(form, false);
    }
}

async function deleteBook(bookId) {
    const book = booksData.find(b => b.id === bookId);
    if (!book) return;
    
    const confirmMessage = `Are you sure you want to delete "${book.title}" by ${book.author}?`;
    
    if (!confirm(confirmMessage)) {
        return;
    }
    
    try {
        await API.deleteBook(bookId);
        
        // Remove from local data
        booksData = booksData.filter(book => book.id !== bookId);
        filterBooks(); // Refresh the display
        
        showToast('Book deleted successfully!', 'success');
        
    } catch (error) {
        console.error('Error deleting book:', error);
        showToast('Error deleting book: ' + error.message, 'danger');
    }
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}
