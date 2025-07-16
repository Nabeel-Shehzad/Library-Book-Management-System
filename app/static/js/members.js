// Members management JavaScript

let membersData = [];
let filteredMembers = [];

document.addEventListener('DOMContentLoaded', function() {
    loadMembers();
    initializeMemberEventListeners();
});

function initializeMemberEventListeners() {
    // Search functionality
    const searchInput = document.getElementById('searchMembers');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(filterMembers, 300));
    }
    
    // Form submissions
    const addMemberForm = document.getElementById('addMemberForm');
    if (addMemberForm) {
        addMemberForm.addEventListener('submit', handleAddMember);
    }
    
    const editMemberForm = document.getElementById('editMemberForm');
    if (editMemberForm) {
        editMemberForm.addEventListener('submit', handleEditMember);
    }
}

async function loadMembers() {
    try {
        showLoadingState(document.getElementById('membersTableBody'));
        membersData = await API.getMembers();
        filteredMembers = [...membersData];
        renderMembersTable();
    } catch (error) {
        console.error('Error loading members:', error);
        showToast('Error loading members: ' + error.message, 'danger');
        document.getElementById('membersTableBody').innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-danger py-4">
                    <i class="fas fa-exclamation-triangle fa-2x mb-3"></i>
                    <br>Error loading members
                </td>
            </tr>
        `;
    }
}

function renderMembersTable() {
    const tbody = document.getElementById('membersTableBody');
    
    if (filteredMembers.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted py-4">
                    <i class="fas fa-users fa-2x mb-3"></i>
                    <br>No members found
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = filteredMembers.map(member => `
        <tr>
            <td>${member.id}</td>
            <td>
                <div class="d-flex align-items-center">
                    <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center me-3" 
                         style="width: 40px; height: 40px; font-weight: bold;">
                        ${getInitials(member.name)}
                    </div>
                    <strong>${escapeHtml(member.name)}</strong>
                </div>
            </td>
            <td>
                <a href="mailto:${escapeHtml(member.email)}" class="text-decoration-none">
                    <i class="fas fa-envelope me-1"></i>
                    ${escapeHtml(member.email)}
                </a>
            </td>
            <td>
                ${member.phone ? `
                    <a href="tel:${escapeHtml(member.phone)}" class="text-decoration-none">
                        <i class="fas fa-phone me-1"></i>
                        ${escapeHtml(member.phone)}
                    </a>
                ` : '<span class="text-muted">N/A</span>'}
            </td>
            <td>${formatDate(member.created_at)}</td>
            <td>
                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-sm btn-outline-success" onclick="editMember(${member.id})" title="Edit Member">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button type="button" class="btn btn-sm btn-outline-info" onclick="viewMemberLoans(${member.id})" title="View Loans">
                        <i class="fas fa-history"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
    
    showLoadingState(tbody, false);
}

function filterMembers() {
    const searchTerm = document.getElementById('searchMembers').value.toLowerCase();
    
    filteredMembers = membersData.filter(member => {
        return !searchTerm || 
            member.name.toLowerCase().includes(searchTerm) ||
            member.email.toLowerCase().includes(searchTerm) ||
            (member.phone && member.phone.toLowerCase().includes(searchTerm));
    });
    
    renderMembersTable();
}

function clearMemberFilters() {
    document.getElementById('searchMembers').value = '';
    filteredMembers = [...membersData];
    renderMembersTable();
}

async function handleAddMember(event) {
    event.preventDefault();
    
    const form = event.target;
    if (!validateForm(form)) {
        showToast('Please fill in all required fields correctly', 'danger');
        return;
    }
    
    const memberData = {
        name: document.getElementById('memberName').value.trim(),
        email: document.getElementById('memberEmail').value.trim(),
        phone: document.getElementById('memberPhone').value.trim() || null
    };
    
    try {
        showLoadingState(form);
        const newMember = await API.createMember(memberData);
        
        // Add to local data
        membersData.push(newMember);
        filterMembers(); // Refresh the display
        
        // Close modal and reset form
        const modal = bootstrap.Modal.getInstance(document.getElementById('addMemberModal'));
        modal.hide();
        clearForm(form);
        
        showToast('Member added successfully!', 'success');
        
    } catch (error) {
        console.error('Error adding member:', error);
        showToast('Error adding member: ' + error.message, 'danger');
    } finally {
        showLoadingState(form, false);
    }
}

async function editMember(memberId) {
    try {
        const member = await API.getMember(memberId);
        
        // Populate edit form
        document.getElementById('editMemberId').value = member.id;
        document.getElementById('editMemberName').value = member.name;
        document.getElementById('editMemberEmail').value = member.email;
        document.getElementById('editMemberPhone').value = member.phone || '';
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('editMemberModal'));
        modal.show();
        
    } catch (error) {
        console.error('Error loading member details:', error);
        showToast('Error loading member details: ' + error.message, 'danger');
    }
}

async function handleEditMember(event) {
    event.preventDefault();
    
    const form = event.target;
    if (!validateForm(form)) {
        showToast('Please fill in all required fields correctly', 'danger');
        return;
    }
    
    const memberId = parseInt(document.getElementById('editMemberId').value);
    const memberData = {
        name: document.getElementById('editMemberName').value.trim(),
        email: document.getElementById('editMemberEmail').value.trim(),
        phone: document.getElementById('editMemberPhone').value.trim() || null
    };
    
    try {
        showLoadingState(form);
        const updatedMember = await API.updateMember(memberId, memberData);
        
        // Update local data
        const index = membersData.findIndex(member => member.id === memberId);
        if (index !== -1) {
            membersData[index] = updatedMember;
            filterMembers(); // Refresh the display
        }
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('editMemberModal'));
        modal.hide();
        
        showToast('Member updated successfully!', 'success');
        
    } catch (error) {
        console.error('Error updating member:', error);
        showToast('Error updating member: ' + error.message, 'danger');
    } finally {
        showLoadingState(form, false);
    }
}

function viewMemberLoans(memberId) {
    const member = membersData.find(m => m.id === memberId);
    if (!member) return;
    
    // For now, show a simple alert. In a full implementation, 
    // this would show a modal with the member's loan history
    showToast(`Loan history for ${member.name} - Feature coming soon!`, 'info');
}

function getInitials(name) {
    return name
        .split(' ')
        .map(word => word.charAt(0).toUpperCase())
        .slice(0, 2)
        .join('');
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
