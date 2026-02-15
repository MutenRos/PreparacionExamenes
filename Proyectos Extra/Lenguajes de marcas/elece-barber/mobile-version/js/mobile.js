// Mobile JavaScript for ELECE Barber
document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile menu
    initMobileMenu();
    
    // Initialize reviews carousel
    initReviewsCarousel();
    
    // Initialize smooth scrolling
    initSmoothScrolling();
    
    // Initialize touch gestures
    initTouchGestures();
});

// Mobile Menu
function initMobileMenu() {
    const menuBtn = document.getElementById('menuBtn');
    const closeBtn = document.getElementById('closeBtn');
    const mobileNav = document.getElementById('mobileNav');
    const overlay = document.getElementById('overlay');
    const navLinks = document.querySelectorAll('.nav-link');

    function openMenu() {
        mobileNav.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        mobileNav.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    menuBtn.addEventListener('click', openMenu);
    closeBtn.addEventListener('click', closeMenu);
    overlay.addEventListener('click', closeMenu);

    // Close menu when clicking on a link
    navLinks.forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    // Swipe to close menu
    let touchStartX = 0;
    let touchEndX = 0;

    mobileNav.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    });

    mobileNav.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        if (touchEndX > touchStartX + 50) {
            closeMenu();
        }
    }
}

// Reviews Carousel
function initReviewsCarousel() {
    const carousel = document.getElementById('reviewsCarousel');
    const dotsContainer = document.getElementById('carouselDots');
    
    if (!carousel || !dotsContainer) return;

    const cards = carousel.querySelectorAll('.review-card');
    
    // Create dots
    cards.forEach((_, index) => {
        const dot = document.createElement('div');
        dot.classList.add('dot');
        if (index === 0) dot.classList.add('active');
        dotsContainer.appendChild(dot);
    });

    const dots = dotsContainer.querySelectorAll('.dot');

    // Update active dot on scroll
    carousel.addEventListener('scroll', () => {
        const scrollLeft = carousel.scrollLeft;
        const cardWidth = cards[0].offsetWidth + 20; // card width + gap
        const activeIndex = Math.round(scrollLeft / cardWidth);

        dots.forEach((dot, index) => {
            if (index === activeIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    });

    // Click on dot to scroll to card
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            const cardWidth = cards[0].offsetWidth + 20;
            carousel.scrollTo({
                left: cardWidth * index,
                behavior: 'smooth'
            });
        });
    });

    // Auto-scroll every 5 seconds
    let autoScrollInterval = setInterval(() => {
        const scrollLeft = carousel.scrollLeft;
        const cardWidth = cards[0].offsetWidth + 20;
        const maxScroll = carousel.scrollWidth - carousel.clientWidth;
        
        if (scrollLeft >= maxScroll - 10) {
            carousel.scrollTo({
                left: 0,
                behavior: 'smooth'
            });
        } else {
            carousel.scrollTo({
                left: scrollLeft + cardWidth,
                behavior: 'smooth'
            });
        }
    }, 5000);

    // Stop auto-scroll on user interaction
    carousel.addEventListener('touchstart', () => {
        clearInterval(autoScrollInterval);
    });
}

// Smooth Scrolling
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Skip if it's just "#"
            if (href === '#') return;
            
            e.preventDefault();
            
            const targetId = href;
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerOffset = 74; // Height of fixed header
                const elementPosition = targetSection.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Touch Gestures
function initTouchGestures() {
    // Add haptic feedback for buttons on touch devices
    const buttons = document.querySelectorAll('button, .btn-primary, .btn-secondary, .action-card');
    
    buttons.forEach(button => {
        button.addEventListener('touchstart', function() {
            // Vibrate if supported (very light feedback)
            if ('vibrate' in navigator) {
                navigator.vibrate(10);
            }
            
            // Visual feedback
            this.style.opacity = '0.8';
        });
        
        button.addEventListener('touchend', function() {
            this.style.opacity = '1';
        });
    });

    // Pull to refresh hint (visual only, no actual refresh)
    let touchStartY = 0;
    let touchEndY = 0;

    document.addEventListener('touchstart', e => {
        touchStartY = e.changedTouches[0].screenY;
    });

    document.addEventListener('touchmove', e => {
        touchEndY = e.changedTouches[0].screenY;
    });

    // Swipe up to hide bottom CTA temporarily
    const bottomCta = document.querySelector('.bottom-cta');
    let lastScrollTop = 0;

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            bottomCta.style.transform = 'translateY(100%)';
        } else {
            // Scrolling up
            bottomCta.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    }, false);
}

// Observe elements for scroll animations
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

// Observe service items, review cards, etc.
document.querySelectorAll('.service-item, .info-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s, transform 0.5s';
    observer.observe(el);
});

// Quick actions pulse animation on load
setTimeout(() => {
    const actionCards = document.querySelectorAll('.action-card');
    actionCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.animation = 'pulse 0.5s';
        }, index * 100);
    });
}, 500);

// Add CSS for pulse animation
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
`;
document.head.appendChild(style);

// Handle iOS Safari address bar hide/show
let resizeTimer;
window.addEventListener('resize', () => {
    // Debounce resize events
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
        
        // Recalculate carousel positions
        const carousel = document.getElementById('reviewsCarousel');
        if (carousel) {
            const scrollLeft = carousel.scrollLeft;
            const cardWidth = carousel.querySelector('.review-card')?.offsetWidth || 0;
            if (cardWidth > 0) {
                const activeIndex = Math.round(scrollLeft / (cardWidth + 20));
                carousel.scrollLeft = activeIndex * (cardWidth + 20);
            }
        }
    }, 250);
});

// Initial call
window.dispatchEvent(new Event('resize'));

// Handle orientation change
window.addEventListener('orientationchange', () => {
    setTimeout(() => {
        window.dispatchEvent(new Event('resize'));
    }, 300);
});

// Prevent zoom on double tap for better UX
let lastTouchEnd = 0;
document.addEventListener('touchend', (event) => {
    const now = Date.now();
    if (now - lastTouchEnd <= 300) {
        event.preventDefault();
    }
    lastTouchEnd = now;
}, { passive: false });

// Fix viewport height on mobile browsers
function setViewportHeight() {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}

setViewportHeight();
window.addEventListener('load', setViewportHeight);
window.addEventListener('resize', setViewportHeight);

// Performance optimization: Lazy load images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Service Worker registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered');
            })
            .catch(err => {
                console.log('SW registration failed');
            });
    });
}
