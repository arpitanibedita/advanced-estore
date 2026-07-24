// API Configuration
const API_BASE_URL = '/api';
let authToken = localStorage.getItem('auth_token');

// Fetch with JWT token
async function apiCall(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
    });
    
    if (response.status === 401) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
        authToken = null;
        window.location.href = '/login';
        return null;
    }
    
    return response.json();
}

// Update navigation based on auth status
function updateNavigation() {
    const authNav = document.getElementById('auth-nav');
    const user = JSON.parse(localStorage.getItem('user'));
    
    if (user && authToken) {
        authNav.innerHTML = `
            <div class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                    ${user.first_name || user.username}
                </a>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                    <li><a class="dropdown-item" href="/dashboard">Dashboard</a></li>
                    <li><a class="dropdown-item" href="/profile">Profile</a></li>
                    ${user.is_admin ? '<li><a class="dropdown-item" href="/admin">Admin Panel</a></li>' : ''}
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#" onclick="logout()">Logout</a></li>
                </ul>
            </div>
        `;
    }
}

// Login
async function login(username_or_email, password) {
    const data = await apiCall('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username_or_email, password })
    });
    
    if (data && data.access_token) {
        authToken = data.access_token;
        localStorage.setItem('auth_token', authToken);
        localStorage.setItem('user', JSON.stringify(data.user));
        updateNavigation();
        return true;
    }
    return false;
}

// Logout
function logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    authToken = null;
    window.location.href = '/';
}

// Load cart count
async function updateCartCount() {
    if (!authToken) return;
    
    const data = await apiCall('/cart');
    if (data) {
        const count = data.count || 0;
        document.getElementById('cart-count').textContent = count;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateNavigation();
    updateCartCount();
});