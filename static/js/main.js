// Skyline Ghana Constructions - Main JavaScript
// Ultra-modern interactions and animations

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initMobileMenu();
    initDropdownMenus();
    initScrollAnimations();
    initSmoothScrolling();
    initFormValidation();
    initImageLightbox();
    initCounterAnimations();
    initParallaxEffects();
    initLoadingStates();
    initImageLazyLoading();
});

// Mobile Menu Toggle
function initMobileMenu() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            const isOpen = mobileMenu.classList.contains('hidden');

            if (isOpen) {
                mobileMenu.classList.remove('hidden');
                mobileMenu.classList.add('animate-fade-in-down');
                mobileMenuButton.setAttribute('aria-expanded', 'true');
            } else {
                mobileMenu.classList.add('hidden');
                mobileMenu.classList.remove('animate-fade-in-down');
                mobileMenuButton.setAttribute('aria-expanded', 'false');
            }
        });
    }
}

// Dropdown Menus
function initDropdownMenus() {
    const servicesDropdown = document.getElementById('services-dropdown');
    const servicesButton = document.getElementById('services-button');
    const servicesMenu = document.getElementById('services-menu');

    if (servicesDropdown && servicesButton && servicesMenu) {
        let hoverTimeout;

        // Handle mouse enter
        servicesDropdown.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimeout);
            showDropdown(servicesButton, servicesMenu);
        });

        // Handle mouse leave
        servicesDropdown.addEventListener('mouseleave', function() {
            hoverTimeout = setTimeout(() => {
                hideDropdown(servicesButton, servicesMenu);
            }, 150); // Small delay to prevent flickering
        });

        // Handle click for mobile/touch devices
        servicesButton.addEventListener('click', function(e) {
            e.preventDefault();
            const isOpen = servicesButton.getAttribute('aria-expanded') === 'true';

            if (isOpen) {
                hideDropdown(servicesButton, servicesMenu);
            } else {
                showDropdown(servicesButton, servicesMenu);
            }
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!servicesDropdown.contains(e.target)) {
                hideDropdown(servicesButton, servicesMenu);
            }
        });

        // Handle keyboard navigation
        servicesButton.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const isOpen = servicesButton.getAttribute('aria-expanded') === 'true';

                if (isOpen) {
                    hideDropdown(servicesButton, servicesMenu);
                } else {
                    showDropdown(servicesButton, servicesMenu);
                }
            } else if (e.key === 'Escape') {
                hideDropdown(servicesButton, servicesMenu);
                servicesButton.focus();
            }
        });
    }
}

function showDropdown(button, menu) {
    button.setAttribute('aria-expanded', 'true');
    menu.classList.remove('opacity-0', 'invisible', 'translate-y-4', 'scale-95');
    menu.classList.add('opacity-100', 'visible', 'translate-y-0', 'scale-100');
}

function hideDropdown(button, menu) {
    button.setAttribute('aria-expanded', 'false');
    menu.classList.remove('opacity-100', 'visible', 'translate-y-0', 'scale-100');
    menu.classList.add('opacity-0', 'invisible', 'translate-y-4', 'scale-95');
}

// Scroll Animations (Optimized)
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                // Stop observing once animated to improve performance
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all elements with animate-on-scroll class
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Smooth Scrolling for anchor links
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Form Validation and Enhancement
function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    let isValid = true;
    let message = '';
    
    // Remove existing error states
    field.classList.remove('border-red-500', 'border-green-500');
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'This field is required';
    }
    
    // Email validation
    if (type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            message = 'Please enter a valid email address';
        }
    }
    
    // Phone validation
    if (type === 'tel' && value) {
        const phoneRegex = /^[\+]?[0-9\s\-\(\)]{10,}$/;
        if (!phoneRegex.test(value)) {
            isValid = false;
            message = 'Please enter a valid phone number';
        }
    }
    
    // Apply validation styles
    if (isValid) {
        field.classList.add('border-green-500');
    } else {
        field.classList.add('border-red-500');
        showFieldError(field, message);
    }
    
    return isValid;
}

function showFieldError(field, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message text-red-500 text-sm mt-1';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

// Image Lightbox
function initImageLightbox() {
    const images = document.querySelectorAll('[data-lightbox]');
    
    images.forEach(img => {
        img.addEventListener('click', function() {
            openLightbox(this.src, this.alt);
        });
    });
}

function openLightbox(src, alt) {
    const lightbox = document.createElement('div');
    lightbox.className = 'fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50 animate-fade-in';
    lightbox.innerHTML = `
        <div class="relative max-w-4xl max-h-full p-4">
            <img src="${src}" alt="${alt}" class="max-w-full max-h-full object-contain">
            <button class="absolute top-4 right-4 text-white text-2xl hover:text-gray-300" onclick="closeLightbox(this)">
                ×
            </button>
        </div>
    `;
    
    document.body.appendChild(lightbox);
    document.body.style.overflow = 'hidden';
    
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) {
            closeLightbox(lightbox.querySelector('button'));
        }
    });
}

function closeLightbox(button) {
    const lightbox = button.closest('.fixed');
    lightbox.remove();
    document.body.style.overflow = '';
}

// Counter Animations
function initCounterAnimations() {
    const counters = document.querySelectorAll('[data-counter]');
    
    const counterObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-counter'));
    const duration = 2000; // 2 seconds
    const increment = target / (duration / 16); // 60fps
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

// Parallax Effects (Optimized with throttling)
function initParallaxEffects() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');

    if (parallaxElements.length > 0) {
        const handleScroll = throttle(() => {
            const scrolled = window.pageYOffset;

            parallaxElements.forEach(element => {
                const rate = scrolled * -0.5;
                element.style.transform = `translateY(${rate}px)`;
            });
        }, 16); // ~60fps

        window.addEventListener('scroll', handleScroll, { passive: true });
    }
}

// Loading States
function initLoadingStates() {
    // Show loading state for forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = `
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                `;
            }
        });
    });
}

// Utility Functions
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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Image Lazy Loading Optimization
function initImageLazyLoading() {
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');

    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.addEventListener('load', () => {
                        img.classList.add('loaded');
                    });
                    observer.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for browsers without IntersectionObserver
        lazyImages.forEach(img => img.classList.add('loaded'));
    }
}

// Expose functions globally for inline event handlers
window.closeLightbox = closeLightbox;
