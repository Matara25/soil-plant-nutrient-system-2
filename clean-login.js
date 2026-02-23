// Clean login fix - remove all conflicts
document.addEventListener('DOMContentLoaded', function() {
    console.log('Clean login script loaded');
    
    // Remove any potential overlays
    const overlays = document.querySelectorAll('.login-background, .bg-pattern, .floating-elements');
    overlays.forEach(overlay => {
        overlay.style.pointerEvents = 'none';
        overlay.style.zIndex = '1';
    });
    
    // Get elements
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginForm = document.getElementById('loginForm');
    const loginBtn = document.querySelector('.login-btn');
    
    // Make login page the top element
    const loginPage = document.getElementById('loginPage');
    if (loginPage) {
        loginPage.style.zIndex = '99999';
        loginPage.style.position = 'fixed';
        loginPage.style.top = '0';
        loginPage.style.left = '0';
        loginPage.style.width = '100%';
        loginPage.style.height = '100%';
        loginPage.style.pointerEvents = 'auto';
    }
    
    // Make login card the top element
    const loginCard = document.querySelector('.login-card');
    if (loginCard) {
        loginCard.style.zIndex = '100000';
        loginCard.style.position = 'relative';
        loginCard.style.pointerEvents = 'auto';
    }
    
    // Force enable inputs with maximum priority
    function forceEnableInput(input, name) {
        if (input) {
            // Remove all disabled states
            input.disabled = false;
            input.readOnly = false;
            input.removeAttribute('disabled');
            input.removeAttribute('readonly');
            
            // Force interaction styles
            input.style.pointerEvents = 'auto';
            input.style.userSelect = 'text';
            input.style.cursor = 'text';
            input.style.webkitUserSelect = 'text';
            input.style.mozUserSelect = 'text';
            input.style.msUserSelect = 'text';
            
            // Force z-index
            input.style.position = 'relative';
            input.style.zIndex = '100001';
            
            // Force visibility
            input.style.visibility = 'visible';
            input.style.opacity = '1';
            
            // Add event listeners to verify
            input.addEventListener('focus', function() {
                console.log(name + ' focused');
                input.style.borderColor = '#8bc34a';
            });
            
            input.addEventListener('input', function(e) {
                console.log(name + ' typed:', e.target.value);
            });
            
            console.log(name + ' force enabled');
        }
    }
    
    // Enable both inputs
    forceEnableInput(usernameInput, 'Username');
    forceEnableInput(passwordInput, 'Password');
    
    // Enable form
    if (loginForm) {
        loginForm.style.pointerEvents = 'auto';
        loginForm.style.zIndex = '100002';
        loginForm.style.position = 'relative';
    }
    
    // Focus username after delay
    setTimeout(() => {
        if (usernameInput) {
            usernameInput.focus();
            console.log('Username focused');
        }
    }, 300);
    
    // Simple login handler
    if (loginBtn) {
        loginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const username = usernameInput ? usernameInput.value.trim() : '';
            const password = passwordInput ? passwordInput.value : '';
            
            console.log('Login attempt:', { username, password });
            
            if ((username === 'farmer' && password === 'soil123') ||
                (username === 'admin' && password === 'admin123') ||
                (username === 'demo' && password === 'demo123')) {
                
                alert('Login successful! Welcome ' + username);
                
                // Hide login page
                document.getElementById('loginPage').style.display = 'none';
                
                // Show main app with all sections
                const mainApp = document.getElementById('mainApp');
                if (mainApp) {
                    mainApp.style.display = 'block';
                    mainApp.style.opacity = '1';
                    mainApp.style.visibility = 'visible';
                    
                    // Show all sections
                    const allSections = document.querySelectorAll('.section-content');
                    allSections.forEach(section => {
                        section.style.display = 'block';
                        section.style.visibility = 'visible';
                        section.style.opacity = '1';
                    });
                    
                    // Show home section by default
                    const homeSection = document.getElementById('home');
                    if (homeSection) {
                        homeSection.classList.add('active-section');
                        homeSection.style.display = 'block';
                    }
                    
                    // Initialize navigation
                    if (typeof initializeApp === 'function') {
                        initializeApp();
                    }
                    
                    console.log('Main app displayed successfully');
                }
                
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
            const type = passwordInput.type === 'password' ? 'text' : 'password';
            passwordInput.type = type;
            toggleBtn.innerHTML = type === 'password' ? 
                '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
        });
    }
    
    console.log('Clean login setup complete');
});
