// Simple direct login fix
document.addEventListener('DOMContentLoaded', function() {
    console.log('Simple login script loaded');
    
    // Get form elements
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginForm = document.getElementById('loginForm');
    const loginBtn = document.querySelector('.login-btn');
    
    // Force enable inputs immediately and keep them enabled
    function enableInput(input, name) {
        if (input) {
            input.disabled = false;
            input.readOnly = false;
            input.style.pointerEvents = 'auto';
            input.style.userSelect = 'auto';
            input.style.cursor = 'text';
            input.style.webkitUserSelect = 'auto';
            input.style.mozUserSelect = 'auto';
            input.style.msUserSelect = 'auto';
            input.style.webkitPointerEvents = 'auto';
            input.style.mozPointerEvents = 'auto';
            input.style.msPointerEvents = 'auto';
            input.removeAttribute('disabled');
            input.removeAttribute('readonly');
            console.log(name + ' field enabled');
        }
    }
    
    // Enable both fields
    enableInput(usernameInput, 'Username');
    enableInput(passwordInput, 'Password');
    
    // Focus username field
    if (usernameInput) {
        setTimeout(() => {
            usernameInput.focus();
            console.log('Username field focused');
        }, 100);
    }
    
    // Keep enabling fields every second (prevents disabling)
    setInterval(() => {
        enableInput(usernameInput, 'Username');
        enableInput(passwordInput, 'Password');
    }, 1000);
    
    if (loginForm) {
        loginForm.style.pointerEvents = 'auto';
        loginForm.style.userSelect = 'auto';
        loginForm.style.zIndex = '9999';
    }
    
    // Simple login handler
    if (loginBtn && loginForm) {
        loginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const username = usernameInput.value.trim();
            const password = passwordInput.value;
            
            console.log('Login attempt:', username, password);
            
            // Demo credentials check
            if ((username === 'farmer' && password === 'soil123') ||
                (username === 'admin' && password === 'admin123') ||
                (username === 'demo' && password === 'demo123')) {
                
                console.log('Login successful!');
                alert('Login successful! Welcome ' + username);
                
                // Hide login page and show main app
                document.getElementById('loginPage').style.display = 'none';
                document.getElementById('mainApp').style.display = 'block';
                
            } else {
                console.log('Login failed!');
                alert('Invalid credentials. Use demo: farmer/soil123');
            }
        });
    }
    
    // Password toggle
    const toggleBtn = document.getElementById('togglePassword');
    if (toggleBtn && passwordInput) {
        toggleBtn.addEventListener('click', function() {
            const type = passwordInput.type === 'password' ? 'text' : 'password';
            passwordInput.type = type;
            toggleBtn.innerHTML = type === 'password' ? 
                '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
        });
    }
    
    console.log('All login elements enabled');
});
