// Login System
class LoginSystem {
    constructor() {
        this.isLoggedIn = false;
        this.currentUser = null;
        this.validCredentials = {
            'farmer': 'soil123',
            'admin': 'admin123',
            'demo': 'demo123'
        };
        this.init();
    }

    init() {
        const savedUser = localStorage.getItem('currentUser');
        const rememberMe = localStorage.getItem('rememberMe');
        
        if (savedUser && rememberMe === 'true') {
            this.login(savedUser, false);
        } else {
            this.showLoginPage();
        }

        this.setupEventListeners();
    }

    setupEventListeners() {
        console.log('Setting up event listeners...');
        
        // Wait a bit to ensure DOM is ready
        setTimeout(() => {
            const loginForm = document.getElementById('loginForm');
            console.log('Login form found:', !!loginForm);
            
            if (loginForm) {
                // Test if form is actually interactive
                loginForm.style.pointerEvents = 'auto';
                loginForm.style.userSelect = 'auto';
                
                loginForm.addEventListener('submit', (e) => {
                    console.log('Form submitted!');
                    e.preventDefault();
                    this.handleLogin();
                });

                // Test individual inputs
                const usernameInput = document.getElementById('username');
                const passwordInput = document.getElementById('password');
                
                if (usernameInput) {
                    console.log('Username input found, adding events...');
                    usernameInput.style.pointerEvents = 'auto';
                    usernameInput.style.userSelect = 'auto';
                    usernameInput.addEventListener('input', (e) => {
                        console.log('Username input:', e.target.value);
                    });
                    usernameInput.addEventListener('focus', () => {
                        console.log('Username input focused');
                    });
                }

                const togglePassword = document.getElementById('togglePassword');
                console.log('Password elements found:', !!togglePassword, !!passwordInput);
                
                if (togglePassword && passwordInput) {
                    console.log('Setting up password toggle...');
                    passwordInput.style.pointerEvents = 'auto';
                    passwordInput.style.userSelect = 'auto';
                    togglePassword.style.pointerEvents = 'auto';
                    
                    togglePassword.addEventListener('click', () => {
                        console.log('Password toggle clicked');
                        const type = passwordInput.type === 'password' ? 'text' : 'password';
                        passwordInput.type = type;
                        togglePassword.innerHTML = type === 'password' ? 
                            '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
                    });
                }

            const logoutBtn = document.getElementById('logoutBtn');
            console.log('Logout button found:', !!logoutBtn);
            
            if (logoutBtn) {
                logoutBtn.addEventListener('click', () => {
                    this.logout();
                });
            }

            const forgotPassword = document.querySelector('.forgot-password');
            if (forgotPassword) {
                forgotPassword.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.showForgotPasswordDialog();
                });
            }

            const signupLink = document.querySelector('.signup-link');
            if (signupLink) {
                signupLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.showSignupDialog();
                });
            }
        }, 500); // Increased delay to ensure DOM is ready
    }

    handleLogin() {
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;
        const rememberMe = document.getElementById('rememberMe').checked;
        const loginBtn = document.querySelector('.login-btn');
        const btnText = loginBtn.querySelector('.btn-text');
        const btnLoader = loginBtn.querySelector('.btn-loader');
        const errorDiv = document.getElementById('loginError');

        console.log('Attempting login with:', { username, password, rememberMe });

        loginBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';
        errorDiv.style.display = 'none';

        setTimeout(() => {
            if (this.authenticate(username, password)) {
                console.log('Login successful!');
                if (rememberMe) {
                    localStorage.setItem('currentUser', username);
                    localStorage.setItem('rememberMe', 'true');
                } else {
                    sessionStorage.setItem('currentUser', username);
                }
                this.login(username, true);
            } else {
                console.log('Login failed!');
                errorDiv.style.display = 'flex';
                loginBtn.disabled = false;
                btnText.style.display = 'inline';
                btnLoader.style.display = 'none';
                
                const loginCard = document.querySelector('.login-card');
                loginCard.style.animation = 'shake 0.5s ease';
                setTimeout(() => {
                    loginCard.style.animation = '';
                }, 500);
            }
        }, 1500);
    }

    authenticate(username, password) {
        return this.validCredentials[username] === password;
    }

    login(username, showAnimation = true) {
        this.isLoggedIn = true;
        this.currentUser = username;
        
        if (showAnimation) {
            this.showMainApp();
        } else {
            this.hideLoginPage();
            this.showMainAppDirect();
        }

        if (typeof initializeApp === 'function') {
            initializeApp();
        }
    }

    logout() {
        this.isLoggedIn = false;
        this.currentUser = null;
        
        localStorage.removeItem('currentUser');
        localStorage.removeItem('rememberMe');
        sessionStorage.removeItem('currentUser');
        
        this.showLoginPage();
        
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.reset();
        }
        
        const errorDiv = document.getElementById('loginError');
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }
    }

    showLoginPage() {
        const loginPage = document.getElementById('loginPage');
        const mainApp = document.getElementById('mainApp');
        
        if (loginPage) {
            loginPage.classList.remove('hidden');
            loginPage.classList.add('active');
        }
        
        if (mainApp) {
            mainApp.style.display = 'none';
            mainApp.classList.remove('active');
        }
        
        document.body.style.overflow = 'hidden';
    }

    hideLoginPage() {
        const loginPage = document.getElementById('loginPage');
        
        if (loginPage) {
            loginPage.classList.add('hidden');
            loginPage.classList.remove('active');
        }
        
        document.body.style.overflow = '';
    }

    showMainApp() {
        const loginPage = document.getElementById('loginPage');
        const mainApp = document.getElementById('mainApp');
        
        if (loginPage) {
            loginPage.classList.add('hidden');
        }
        
        setTimeout(() => {
            if (mainApp) {
                mainApp.style.display = 'block';
                setTimeout(() => {
                    mainApp.classList.add('active');
                }, 50);
            }
            
            document.body.style.overflow = '';
        }, 500);
    }

    showMainAppDirect() {
        const loginPage = document.getElementById('loginPage');
        const mainApp = document.getElementById('mainApp');
        
        if (loginPage) {
            loginPage.style.display = 'none';
            loginPage.classList.add('hidden');
        }
        
        if (mainApp) {
            mainApp.style.display = 'block';
            mainApp.classList.add('active');
        }
        
        document.body.style.overflow = '';
    }

    showForgotPasswordDialog() {
        showLoginNotification('Password reset feature coming soon! Please contact support.', 'info');
    }

    showSignupDialog() {
        showLoginNotification('Account registration feature coming soon! Please use demo credentials.', 'info');
    }
}

// Initialize login system when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing login system...');
    const loginSystem = new LoginSystem();
    
    // Make login system globally available
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(loginAnimationStyles);
