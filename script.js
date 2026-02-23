// Wait for DOM to be ready before initializing
document.addEventListener('DOMContentLoaded', () => {
    // Check if login system exists before using it
    if (typeof window.loginSystem !== 'undefined') {
        // Login system is already initialized by login.js
        console.log('Login system initialized');
    }
    
    // Initialize main application
    initializeApp();
});

// Main Application Initialization
function initializeApp() {
    // Set up navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionId = link.getAttribute('data-section');
            if (sectionId) {
                showSection(sectionId);
            }
        });
    });
    
    // Show home section by default
    showSection('home');
    
    // Handle browser back/forward buttons
    window.addEventListener('popstate', (e) => {
        if (e.state && e.state.section) {
            showSection(e.state.section);
        }
    });
}

// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Single Page Application Navigation
function showSection(sectionId) {
    // Hide all sections
    const allSections = document.querySelectorAll('.section-content');
    allSections.forEach(section => {
        section.classList.remove('active-section');
        section.style.display = 'none';
    });
    
    // Show selected section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active-section');
        targetSection.style.display = 'block';
        
        // Scroll to top of section
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        // Update active nav link
        updateActiveNavLink(sectionId);
        
        // Initialize section-specific features
        initializeSection(sectionId);
    }
}

// Update active navigation link
function updateActiveNavLink(sectionId) {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-section') === sectionId) {
            link.classList.add('active');
        }
    });
}

// Initialize section-specific features
function initializeSection(sectionId) {
    switch(sectionId) {
        case 'farmers-dashboard':
            initializeFarmersDashboard();
            break;
        case 'sensor-dashboard':
            initializeSensorDashboard();
            break;
        case 'recommendation-dashboard':
            initializeRecommendationDashboard();
            break;
        case 'home':
            // Re-initialize hero animations
            initializeHeroSection();
            break;
    }
}

// Farmers Dashboard Initialization
function initializeFarmersDashboard() {
    // Animate stats
    animateDashboardStats();
    
    // Initialize crop progress bars
    initializeCropProgress();
    
    // Add interactivity to action buttons
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach(btn => {
        btn.addEventListener('click', handleActionClick);
    });
}

// Sensor Dashboard Initialization
function initializeSensorDashboard() {
    // Start real-time data simulation
    startSensorDataSimulation();
    
    // Initialize sensor charts
    initializeSensorCharts();
    
    // Add refresh functionality
    const refreshBtn = document.querySelector('.refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', refreshSensorData);
    }
}

// Recommendation Dashboard Initialization
function initializeRecommendationDashboard() {
    // Animate recommendation cards
    animateRecommendationCards();
    
    // Add click handlers for fertilizer recommendations
    const fertilizerButtons = document.querySelectorAll('.fertilizer-action .btn');
    fertilizerButtons.forEach(btn => {
        btn.addEventListener('click', handleFertilizerAction);
    });
}

// Hero Section Initialization
function initializeHeroSection() {
    // Re-trigger hero animations
    const heroElements = document.querySelectorAll('.hero-content, .hero-graphic');
    heroElements.forEach((el, index) => {
        el.style.animation = 'none';
        setTimeout(() => {
            el.style.animation = `fadeInUp 1s ease ${index * 0.2}s both`;
        }, 100);
    });
}

// Navigation event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Set up navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionId = link.getAttribute('data-section');
            if (sectionId) {
                showSection(sectionId);
            }
        });
    });
    
    // Show home section by default
    showSection('home');
    
    // Handle browser back/forward buttons
    window.addEventListener('popstate', (e) => {
        if (e.state && e.state.section) {
            showSection(e.state.section);
        }
    });
});

// Dashboard utility functions
function animateDashboardStats() {
    const statValues = document.querySelectorAll('.stat-value');
    statValues.forEach(stat => {
        const finalValue = stat.textContent;
        if (!isNaN(finalValue)) {
            animateCounter(stat, parseInt(finalValue));
        }
    });
}

function initializeCropProgress() {
    const progressBars = document.querySelectorAll('.progress');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.transition = 'width 1s ease';
            bar.style.width = width;
        }, 100);
    });
}

function handleActionClick(e) {
    const buttonText = e.currentTarget.querySelector('span').textContent;
    showNotification(`${buttonText} feature coming soon!`, 'info');
}

// Sensor dashboard functions
function startSensorDataSimulation() {
    // Simulate real-time sensor updates
    setInterval(() => {
        updateSensorValues();
    }, 5000);
}

function updateSensorValues() {
    const sensorValues = document.querySelectorAll('.sensor-value .value');
    sensorValues.forEach(value => {
        const currentValue = parseFloat(value.textContent);
        const variation = (Math.random() - 0.5) * 0.1;
        const newValue = Math.max(0, currentValue + variation);
        value.textContent = newValue.toFixed(1);
    });
}

function initializeSensorCharts() {
    // Simple chart visualization using CSS
    const charts = document.querySelectorAll('.sensor-chart');
    charts.forEach(chart => {
        chart.innerHTML = '<div class="mini-chart"></div>';
    });
}

function refreshSensorData() {
    const refreshBtn = document.querySelector('.refresh-btn i');
    refreshBtn.style.animation = 'spin 1s ease';
    
    setTimeout(() => {
        updateSensorValues();
        refreshBtn.style.animation = 'none';
        showNotification('Sensor data refreshed!', 'success');
    }, 1000);
}

// Recommendation dashboard functions
function animateRecommendationCards() {
    const cards = document.querySelectorAll('.fertilizer-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 200);
    });
}

function handleFertilizerAction(e) {
    const fertilizerName = e.target.closest('.fertilizer-card').querySelector('h4').textContent;
    showNotification(`Applied recommendation: ${fertilizerName}`, 'success');
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        background: ${type === 'success' ? 'var(--accent-green)' : type === 'error' ? '#e74c3c' : '#3498db'};
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .section-content {
        display: none;
        min-height: 100vh;
        padding-top: 70px;
    }
    
    .section-content.active-section {
        display: block;
    }
    
    .nav-link.active {
        color: var(--secondary-green) !important;
    }
    
    .nav-link.active::after {
        width: 100% !important;
    }
    
    .mini-chart {
        height: 40px;
        background: linear-gradient(45deg, 
            var(--accent-green) 25%, 
            transparent 25%, 
            transparent 50%, 
            var(--accent-green) 50%, 
            var(--accent-green) 75%, 
            transparent 75%);
        background-size: 20px 20px;
        border-radius: 4px;
        opacity: 0.3;
    }
`;
document.head.appendChild(style);

// Smooth scrolling for anchor links (if any remain)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        if (!this.getAttribute('data-section')) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Navbar background on scroll
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
    }
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.about-card, .tech-item, .step, .layer, .stat-card');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Counter animation for statistics
const animateCounter = (element, target, duration = 2000) => {
    let start = 0;
    const increment = target / (duration / 16);
    
    const updateCounter = () => {
        start += increment;
        if (start < target) {
            element.textContent = Math.ceil(start) + (element.textContent.includes('%') ? '%' : '');
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target + (element.textContent.includes('%') ? '%' : '');
        }
    };
    
    updateCounter();
};

// Trigger counter animation when statistics section is visible
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
            const statNumbers = entry.target.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {
                const text = stat.textContent;
                const number = parseInt(text.replace(/\D/g, ''));
                if (!isNaN(number)) {
                    animateCounter(stat, number);
                }
            });
            entry.target.classList.add('animated');
        }
    });
}, { threshold: 0.5 });

const achievementsSection = document.querySelector('.achievements');
if (achievementsSection) {
    statsObserver.observe(achievementsSection);
}

// Form submission handling
const contactForm = document.querySelector('.contact-form form');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(contactForm);
        const data = Object.fromEntries(formData);
        
        // Show success message
        const successMessage = document.createElement('div');
        successMessage.className = 'success-message';
        successMessage.textContent = 'Thank you for your interest! We will contact you soon.';
        successMessage.style.cssText = `
            background: linear-gradient(135deg, #4a7c28, #8bc34a);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
            font-weight: 500;
            animation: fadeInUp 0.5s ease;
        `;
        
        contactForm.appendChild(successMessage);
        contactForm.reset();
        
        // Remove success message after 5 seconds
        setTimeout(() => {
            successMessage.remove();
        }, 5000);
    });
}

// Add hover effect to cards
document.querySelectorAll('.about-card, .tech-item, .step, .layer, .stat-card, .dashboard-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero && hero.classList.contains('active-section')) {
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// Add loading animation
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Button ripple effect
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            left: ${x}px;
            top: ${y}px;
            pointer-events: none;
            transform: scale(0);
            animation: ripple 0.6s ease-out;
        `;
        
        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// Add CSS for ripple animation
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);

// Smooth reveal for sections on scroll
const revealSections = () => {
    const sections = document.querySelectorAll('.section-content');
    
    sections.forEach(section => {
        const sectionTop = section.getBoundingClientRect().top;
        const sectionBottom = section.getBoundingClientRect().bottom;
        
        if (sectionTop < window.innerHeight && sectionBottom > 0) {
            section.classList.add('revealed');
        }
    });
};

window.addEventListener('scroll', revealSections);
window.addEventListener('load', revealSections);

// Add keyboard navigation support
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    }
});

// Performance optimization - Debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Apply debouncing to scroll events
const debouncedScroll = debounce(() => {
    // Scroll-related functions here
}, 10);

window.addEventListener('scroll', debouncedScroll);

// Add touch support for mobile devices
if ('ontouchstart' in window) {
    document.body.classList.add('touch-device');
}

// Lazy loading for images (if any are added later)
const lazyImages = document.querySelectorAll('img[data-src]');
const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            imageObserver.unobserve(img);
        }
    });
});

lazyImages.forEach(img => imageObserver.observe(img));
