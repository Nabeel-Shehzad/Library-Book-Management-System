// Loans management JavaScript

let availableBooks = [];
let allMembers = [];

document.addEventListener('DOMContentLoaded', function() {
    loadLoansPageData();
    initializeLoansEventListeners();
});

function initializeLoansEventListeners() {
    // Form submissions
    const newLoanForm = document.getElementById('newLoanForm');
    if (newLoanForm) {
        newLoanForm.addEventListener('submit', handleNewLoan);
    }
    
    const returnBookForm = document.getElementById('returnBookForm');
    if (returnBookForm) {
        returnBookForm.addEventListener('submit', handleReturnBook);
    }
}

async function loadLoansPageData() {
    try {
        // Load all books and filter available ones
        const allBooks = await API.getBooks();
        availableBooks = allBooks.filter(book => book.available);
        
        // Load all members
        allMembers = await API.getMembers();
        
        // Load current active loans
        await loadCurrentLoans();
        
        // Render the page
        renderAvailableBooks();
        populateBookSelect();
        populateMemberSelect();
        
    } catch (error) {
        console.error('Error loading loans page data:', error);
        showToast('Error loading data: ' + error.message, 'danger');
    }
}

function renderAvailableBooks() {
    const container = document.getElementById('availableBooksRow');
    
    if (availableBooks.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center py-4">
                <i class="fas fa-book fa-2x text-muted mb-3"></i>
                <h5 class="text-muted">No books available for loan</h5>
                <p class="text-muted">All books are currently borrowed or no books exist in the system.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = availableBooks.map(book => `
        <div class="col-md-4 col-lg-3 mb-3">
            <div class="card book-card h-100" onclick="selectBookForLoan(${book.id})">
                <div class="card-body">
                    <h6 class="card-title text-truncate-2" title="${escapeHtml(book.title)}">
                        <i class="fas fa-book text-primary me-2"></i>
                        ${escapeHtml(book.title)}
                    </h6>
                    <p class="card-text">
                        <small class="text-muted">
                            <i class="fas fa-user me-1"></i>
                            ${escapeHtml(book.author)}
                        </small>
                    </p>
                    ${book.isbn ? `
                        <p class="card-text">
                            <small class="text-muted">
                                <i class="fas fa-barcode me-1"></i>
                                ${book.isbn}
                            </small>
                        </p>
                    ` : ''}
                    <span class="badge bg-success">
                        <i class="fas fa-check-circle me-1"></i>
                        Available
                    </span>
                </div>
            </div>
        </div>
    `).join('');
}

function populateBookSelect() {
    const select = document.getElementById('loanBookSelect');
    if (!select) return;
    
    // Clear existing options except the first one
    select.innerHTML = '<option value="">Choose a book...</option>';
    
    availableBooks.forEach(book => {
        const option = document.createElement('option');
        option.value = book.id;
        option.textContent = `${book.title} by ${book.author}`;
        select.appendChild(option);
    });
}

function populateMemberSelect() {
    const select = document.getElementById('loanMemberSelect');
    if (!select) return;
    
    // Clear existing options except the first one
    select.innerHTML = '<option value="">Choose a member...</option>';
    
    allMembers.forEach(member => {
        const option = document.createElement('option');
        option.value = member.id;
        option.textContent = `${member.name} (${member.email})`;
        select.appendChild(option);
    });
}

function selectBookForLoan(bookId) {
    // Remove selection from all cards
    document.querySelectorAll('.book-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Add selection to clicked card
    event.currentTarget.classList.add('selected');
    
    // Set the book in the modal select
    const bookSelect = document.getElementById('loanBookSelect');
    if (bookSelect) {
        bookSelect.value = bookId;
    }
    
    // Show the new loan modal
    const modal = new bootstrap.Modal(document.getElementById('newLoanModal'));
    modal.show();
}

async function handleNewLoan(event) {
    event.preventDefault();
    
    const form = event.target;
    if (!validateForm(form)) {
        showToast('Please select both a book and a member', 'danger');
        return;
    }
    
    const loanData = {
        book_id: parseInt(document.getElementById('loanBookSelect').value),
        member_id: parseInt(document.getElementById('loanMemberSelect').value)
    };
    
    try {
        showLoadingState(form);
        const loan = await API.createLoan(loanData);
        
        // Remove the book from available books
        availableBooks = availableBooks.filter(book => book.id !== loanData.book_id);
        
        // Re-render the page
        renderAvailableBooks();
        populateBookSelect();
        
        // Close modal and reset form
        const modal = bootstrap.Modal.getInstance(document.getElementById('newLoanModal'));
        modal.hide();
        clearForm(form);
        
        // Remove selection from cards
        document.querySelectorAll('.book-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        showToast(`Book loaned successfully! Loan ID: ${loan.loan_id}`, 'success');
        
        // Show loan details
        showLoanDetails(loan);
        
    } catch (error) {
        console.error('Error creating loan:', error);
        showToast('Error creating loan: ' + error.message, 'danger');
    } finally {
        showLoadingState(form, false);
    }
}

async function handleReturnBook(event) {
    event.preventDefault();
    
    const form = event.target;
    if (!validateForm(form)) {
        showToast('Please enter a loan ID', 'danger');
        return;
    }
    
    const returnData = {
        loan_id: parseInt(document.getElementById('returnLoanId').value)
    };
    
    try {
        showLoadingState(form);
        const returnResult = await API.returnBook(returnData);
        
        // Reload the page data to refresh available books
        await loadLoansPageData();
        
        // Close modal and reset form
        const modal = bootstrap.Modal.getInstance(document.getElementById('returnBookModal'));
        modal.hide();
        clearForm(form);
        
        showToast('Book returned successfully!', 'success');
        
        // Show return details
        showReturnDetails(returnResult);
        
    } catch (error) {
        console.error('Error returning book:', error);
        showToast('Error returning book: ' + error.message, 'danger');
    } finally {
        showLoadingState(form, false);
    }
}

async function loadCurrentLoans() {
    try {
        const loans = await API.getLoans();
        const activeLoans = loans.filter(loan => loan.status === 'active');
        renderCurrentLoans(activeLoans);
    } catch (error) {
        console.error('Error loading current loans:', error);
        const currentLoansSection = document.getElementById('currentLoansSection');
        currentLoansSection.innerHTML = `
            <div class="text-center py-4 text-danger">
                <i class="fas fa-exclamation-triangle fa-2x mb-3"></i>
                <br>Error loading current loans
            </div>
        `;
    }
}

function renderCurrentLoans(activeLoans) {
    const currentLoansSection = document.getElementById('currentLoansSection');
    
    if (activeLoans.length === 0) {
        currentLoansSection.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-info-circle fa-2x text-muted mb-3"></i>
                <br>No active loans at the moment
            </div>
        `;
        return;
    }
    
    const loansHtml = activeLoans.map(loan => {
        // Find book and member details
        const allBooks = [...availableBooks]; // Available books
        // We need to get borrowed books too, so let's use a different approach
        const book = { id: loan.book_id, title: 'Loading...', author: 'Loading...' };
        const member = allMembers.find(m => m.id === loan.member_id) || { name: 'Unknown Member' };
        
        return `
            <div class="card mb-3">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md-8">
                            <h6 class="card-title mb-1">
                                <i class="fas fa-book text-primary me-2"></i>
                                <span id="book-title-${loan.book_id}">${escapeHtml(book.title)}</span>
                            </h6>
                            <p class="card-text mb-1">
                                <small class="text-muted">
                                    <i class="fas fa-user me-1"></i>
                                    Author: <span id="book-author-${loan.book_id}">${escapeHtml(book.author)}</span>
                                </small>
                            </p>
                            <p class="card-text mb-1">
                                <small class="text-muted">
                                    <i class="fas fa-user-circle me-1"></i>
                                    Borrowed by: ${escapeHtml(member.name)}
                                </small>
                            </p>
                            <p class="card-text mb-0">
                                <small class="text-muted">
                                    <i class="fas fa-calendar me-1"></i>
                                    Borrowed on: ${formatDateTime(loan.borrowed_at)}
                                </small>
                            </p>
                        </div>
                        <div class="col-md-4 text-end">
                            <button type="button" class="btn btn-success btn-sm" onclick="quickReturnBook(${loan.id})" title="Return Book">
                                <i class="fas fa-undo me-1"></i>Return
                            </button>
                            <br>
                            <span class="badge bg-warning mt-2">
                                <i class="fas fa-clock me-1"></i>Active
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    currentLoansSection.innerHTML = loansHtml;
    
    // Load book details for each loan
    activeLoans.forEach(async (loan) => {
        try {
            const book = await API.getBook(loan.book_id);
            const titleElement = document.getElementById(`book-title-${loan.book_id}`);
            const authorElement = document.getElementById(`book-author-${loan.book_id}`);
            if (titleElement) titleElement.textContent = book.title;
            if (authorElement) authorElement.textContent = book.author;
        } catch (error) {
            console.error(`Error loading book ${loan.book_id}:`, error);
        }
    });
}

function quickReturnBook(loanId) {
    // Set the loan ID in the return modal and show it
    const returnLoanIdInput = document.getElementById('returnLoanId');
    if (returnLoanIdInput) {
        returnLoanIdInput.value = loanId;
    }
    
    const returnModal = new bootstrap.Modal(document.getElementById('returnBookModal'));
    returnModal.show();
}

function showLoanDetails(loan) {
    const book = availableBooks.find(b => b.id === loan.book_id) || 
                  { title: 'Unknown Book', author: 'Unknown Author' };
    const member = allMembers.find(m => m.id === loan.member_id) || 
                   { name: 'Unknown Member' };
    
    const details = `
        <div class="alert alert-info alert-dismissible fade show" role="alert">
            <h5><i class="fas fa-handshake me-2"></i>Loan Created</h5>
            <hr>
            <p><strong>Loan ID:</strong> ${loan.loan_id}</p>
            <p><strong>Book:</strong> ${escapeHtml(book.title)} by ${escapeHtml(book.author)}</p>
            <p><strong>Member:</strong> ${escapeHtml(member.name)}</p>
            <p><strong>Borrowed At:</strong> ${formatDateTime(loan.borrowed_at)}</p>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const currentLoansSection = document.getElementById('currentLoansSection');
    currentLoansSection.innerHTML = details + currentLoansSection.innerHTML;
}

function showReturnDetails(returnResult) {
    const book = availableBooks.find(b => b.id === returnResult.book_id) || 
                  { title: 'Unknown Book', author: 'Unknown Author' };
    const member = allMembers.find(m => m.id === returnResult.member_id) || 
                   { name: 'Unknown Member' };
    
    const details = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            <h5><i class="fas fa-undo me-2"></i>Book Returned</h5>
            <hr>
            <p><strong>Loan ID:</strong> ${returnResult.loan_id}</p>
            <p><strong>Book:</strong> ${escapeHtml(book.title)} by ${escapeHtml(book.author)}</p>
            <p><strong>Member:</strong> ${escapeHtml(member.name)}</p>
            <p><strong>Borrowed At:</strong> ${formatDateTime(returnResult.borrowed_at)}</p>
            <p><strong>Returned At:</strong> ${formatDateTime(returnResult.returned_at)}</p>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const currentLoansSection = document.getElementById('currentLoansSection');
    currentLoansSection.innerHTML = details + currentLoansSection.innerHTML;
}

function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}
