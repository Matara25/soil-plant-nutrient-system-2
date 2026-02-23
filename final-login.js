// Final simple login fix - no loops, direct approach
document.addEventListener('DOMContentLoaded', function() {
    console.log('Final login script loaded');
    
    // Get elements
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginForm = document.getElementById('loginForm');
    const loginBtn = document.querySelector('.login-btn');
    
    // Remove any overlays that might block interaction
    const overlays = document.querySelectorAll('.login-page.hidden, .login-overlay');
    overlays.forEach(overlay => overlay.remove());
    
    // Make sure login page is visible and interactive
    const loginPage = document.getElementById('loginPage');
    if (loginPage) {
        loginPage.style.display = 'flex';
        loginPage.style.visibility = 'visible';
        loginPage.style.opacity = '1';
        loginPage.style.pointerEvents = 'auto';
    }
    
    // Direct input enabling - no functions, no loops
    if (usernameInput) {
        usernameInput.disabled = false;
        usernameInput.readOnly = false;
        usernameInput.style.pointerEvents = 'auto';
        usernameInput.style.userSelect = 'text';
        usernameInput.style.cursor = 'text';
        usernameInput.style.webkitUserSelect = 'text';
        usernameInput.style.mozUserSelect = 'text';
        usernameInput.style.msUserSelect = 'text';
        usernameInput.removeAttribute('disabled');
        usernameInput.removeAttribute('readonly');
        usernameInput.tabIndex = '1';
        console.log('Username field directly enabled');
    }
    
    if (passwordInput) {
        passwordInput.disabled = false;
        passwordInput.readOnly = false;
        passwordInput.style.pointerEvents = 'auto';
        passwordInput.style.userSelect = 'text';
        passwordInput.style.cursor = 'text';
        passwordInput.style.webkitUserSelect = 'text';
        passwordInput.style.mozUserSelect = 'text';
        passwordInput.style.msUserSelect = 'text';
        passwordInput.removeAttribute('disabled');
        passwordInput.removeAttribute('readonly');
        passwordInput.tabIndex = '2';
        console.log('Password field directly enabled');
    }
    
    // Enable form
    if (loginForm) {
        loginForm.disabled = false;
        loginForm.style.pointerEvents = 'auto';
        loginForm.style.userSelect = 'auto';
        loginForm.removeAttribute('disabled');
    }
    
    // Focus username after a short delay
    setTimeout(() => {
        if (usernameInput) {
            usernameInput.focus();
            console.log('Username field focused');
        }
    }, 200);
    
    // Simple login - no complex logic
    if (loginBtn) {
        loginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const username = usernameInput ? usernameInput.value.trim() : '';
            const password = passwordInput ? passwordInput.value : '';
            
            console.log('Login attempt:', { username, password });
            
            // Demo credentials
            if ((username === 'farmer' && password === 'soil123') ||
                (username === 'admin' && password === 'admin123') ||
                (username === 'demo' && password === 'demo123')) {
                
                alert('Login successful! Welcome ' + username);
                document.getElementById('loginPage').style.display = 'none';
                document.getElementById('mainApp').style.display = 'block';
                
            } else {
                alert('Invalid credentials. Use: farmer/soil123');
            }
        });
    }
    
    // Password toggle
    const toggleBtn = document.getElementById('togglePassword');
    if (toggleBtn && passwordInput) {
        toggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const type = passwordInput.type === 'password' ? 'text' : 'password';
            passwordInput.type = type;
            toggleBtn.innerHTML = type === 'password' ? 
                '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
        });
    }
    
    console.log('Final login setup complete - no loops');
});
