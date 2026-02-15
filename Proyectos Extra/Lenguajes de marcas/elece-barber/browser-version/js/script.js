// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu functionality
    initMobileMenu();
    
    // Smooth scrolling for navigation links
    initSmoothScrolling();
    
    // Navbar scroll effect
    initNavbarScrollEffect();
    
    // Scroll animations
    initScrollAnimations();
    
    // Gallery lightbox
    initGalleryLightbox();
    
    // Instagram feed
    initInstagramFeed();
    
    // Reviews carousel
    initReviewsCarousel();
    
    // Contact form functionality
    initContactForm();
    
    // Business hours highlight
    initBusinessHours();
    
    // Loading animations
    initLoadingAnimations();
    
    // Back to top button
    initBackToTop();
    
    // Advanced interactions
    initAdvancedInteractions();
});

// Mobile Menu Functionality
function initMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
            
            // Animate hamburger bars
            const bars = hamburger.querySelectorAll('.bar');
            bars.forEach((bar, index) => {
                if (hamburger.classList.contains('active')) {
                    if (index === 0) bar.style.transform = 'rotate(45deg) translate(5px, 5px)';
                    if (index === 1) bar.style.opacity = '0';
                    if (index === 2) bar.style.transform = 'rotate(-45deg) translate(7px, -6px)';
                } else {
                    bar.style.transform = 'none';
                    bar.style.opacity = '1';
                }
            });
        });

        // Close mobile menu when clicking on a link
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
                
                // Reset hamburger animation
                const bars = hamburger.querySelectorAll('.bar');
                bars.forEach(bar => {
                    bar.style.transform = 'none';
                    bar.style.opacity = '1';
                });
            });
        });
    }
}

// Smooth Scrolling for Navigation Links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerOffset = 140; // Height of fixed navbar (increased)
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

// Navbar Scroll Effect
function initNavbarScrollEffect() {
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;

    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add/remove background based on scroll position
        if (scrollTop > 50) {
            navbar.style.background = 'rgba(0, 0, 0, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.3)';
        } else {
            navbar.style.background = 'rgba(0, 0, 0, 0.95)';
            navbar.style.boxShadow = 'none';
        }

        // Hide/show navbar on scroll (optional)
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });
}

// Advanced Scroll Animations with Intersection Observer
function initScrollAnimations() {
    const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');
    const animatedElements = document.querySelectorAll('.service-card, .review-card, .contact-item, .about-content, .about-image');
    
    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add stagger delay for better visual effect
                setTimeout(() => {
                    entry.target.classList.add('active');
                }, index * 100);
                
                // Unobserve after animation to improve performance
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe reveal elements
    revealElements.forEach(element => {
        observer.observe(element);
    });
    
    // Add reveal classes to animated elements
    animatedElements.forEach((element, index) => {
        if (!element.classList.contains('reveal') && 
            !element.classList.contains('reveal-left') && 
            !element.classList.contains('reveal-right') &&
            !element.classList.contains('reveal-scale')) {
            
            // Alternate animation directions for visual interest
            if (index % 3 === 0) {
                element.classList.add('reveal-left');
            } else if (index % 3 === 1) {
                element.classList.add('reveal-right');
            } else {
                element.classList.add('reveal-scale');
            }
            
            observer.observe(element);
        }
    });
    
    // Parallax effect for hero section
    initParallaxEffect();
    
    // Add scroll progress indicator
    initScrollProgress();
}

// Parallax Effect
function initParallaxEffect() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxSpeed = 0.5;
        
        if (scrolled < window.innerHeight) {
            hero.style.transform = `translateY(${scrolled * parallaxSpeed}px)`;
            hero.style.opacity = 1 - (scrolled / window.innerHeight) * 0.5;
        }
    });
}

// Scroll Progress Indicator
function initScrollProgress() {
    // Create progress bar element
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    progressBar.innerHTML = '<div class="scroll-progress-bar"></div>';
    document.body.appendChild(progressBar);
    
    // Update progress on scroll
    window.addEventListener('scroll', () => {
        const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (window.pageYOffset / windowHeight) * 100;
        document.querySelector('.scroll-progress-bar').style.width = scrolled + '%';
    });
}

// Gallery Lightbox Functionality
function initGalleryLightbox() {
    const galleryItems = document.querySelectorAll('.gallery-item:not(.instagram-post)');
    const instagramPosts = document.querySelectorAll('.instagram-post');
    
    // Regular gallery items
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const lightbox = createLightbox();
            const img = this.querySelector('.gallery-placeholder');
            
            if (img) {
                const lightboxContent = lightbox.querySelector('.lightbox-content');
                const clonedImg = img.cloneNode(true);
                clonedImg.style.maxWidth = '90vw';
                clonedImg.style.maxHeight = '90vh';
                lightboxContent.appendChild(clonedImg);
                
                document.body.appendChild(lightbox);
                
                // Show lightbox with animation
                setTimeout(() => {
                    lightbox.style.opacity = '1';
                    lightbox.querySelector('.lightbox-content').style.transform = 'scale(1)';
                }, 10);
            }
        });
    });
    
    // Instagram posts - redirect to Instagram
    instagramPosts.forEach(post => {
        post.addEventListener('click', function() {
            window.open('https://www.instagram.com/elecebarber_/', '_blank');
        });
    });
}

function createLightbox() {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 2000;
        opacity: 0;
        transition: opacity 0.3s ease;
        cursor: pointer;
    `;
    
    const lightboxContent = document.createElement('div');
    lightboxContent.className = 'lightbox-content';
    lightboxContent.style.cssText = `
        transform: scale(0.8);
        transition: transform 0.3s ease;
        position: relative;
    `;
    
    const closeButton = document.createElement('button');
    closeButton.innerHTML = '&times;';
    closeButton.style.cssText = `
        position: absolute;
        top: -40px;
        right: -40px;
        background: none;
        border: none;
        color: white;
        font-size: 2rem;
        cursor: pointer;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    
    lightboxContent.appendChild(closeButton);
    lightbox.appendChild(lightboxContent);
    
    // Close lightbox functionality
    const closeLightbox = () => {
        lightbox.style.opacity = '0';
        setTimeout(() => {
            if (lightbox.parentNode) {
                lightbox.parentNode.removeChild(lightbox);
            }
        }, 300);
    };
    
    lightbox.addEventListener('click', closeLightbox);
    closeButton.addEventListener('click', closeLightbox);
    
    // Prevent closing when clicking on content
    lightboxContent.addEventListener('click', (e) => {
        e.stopPropagation();
    });
    
    return lightbox;
}

// Instagram Feed Functionality
function initInstagramFeed() {
    // Placeholder function for Instagram feed
    // In a real implementation, you would use Instagram Basic Display API
    // or a third-party service like Instafeed.js
    
    const instagramFeed = document.getElementById('instagram-feed');
    const placeholderGrid = document.querySelector('.gallery-placeholder-grid');
    
    // Add hover effects to Instagram posts
    const instagramPosts = document.querySelectorAll('.instagram-post');
    instagramPosts.forEach(post => {
        post.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        post.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Add loading animation
    if (placeholderGrid) {
        placeholderGrid.style.opacity = '0.7';
        setTimeout(() => {
            placeholderGrid.style.opacity = '1';
        }, 500);
    }
}

// Reviews Carousel Functionality
function initReviewsCarousel() {
    const carousel = document.getElementById('reviews-carousel');
    const prevBtn = document.querySelector('.carousel-btn-prev');
    const nextBtn = document.querySelector('.carousel-btn-next');
    const indicatorsContainer = document.getElementById('carousel-indicators');
    
    if (!carousel) return;
    
    const cards = carousel.querySelectorAll('.review-card');
    const cardWidth = 350 + 30; // card width + gap
    let currentIndex = 0;
    
    // Create indicators
    createIndicators();
    
    // Event listeners for buttons
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            currentIndex = Math.max(0, currentIndex - 1);
            updateCarousel();
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            currentIndex = Math.min(cards.length - getVisibleCards(), currentIndex + 1);
            updateCarousel();
        });
    }
    
    // Auto-scroll functionality
    let autoScrollInterval = setInterval(autoScroll, 5000);
    
    // Pause auto-scroll on hover
    carousel.addEventListener('mouseenter', () => {
        clearInterval(autoScrollInterval);
    });
    
    carousel.addEventListener('mouseleave', () => {
        autoScrollInterval = setInterval(autoScroll, 5000);
    });
    
    // Touch/swipe support for mobile
    let startX = 0;
    let scrollLeft = 0;
    
    carousel.addEventListener('touchstart', (e) => {
        startX = e.touches[0].pageX - carousel.offsetLeft;
        scrollLeft = carousel.scrollLeft;
    });
    
    carousel.addEventListener('touchmove', (e) => {
        if (!startX) return;
        e.preventDefault();
        const x = e.touches[0].pageX - carousel.offsetLeft;
        const walk = (x - startX) * 2;
        carousel.scrollLeft = scrollLeft - walk;
    });
    
    carousel.addEventListener('touchend', () => {
        startX = 0;
        updateIndicatorsFromScroll();
    });
    
    // Update indicators based on scroll position
    carousel.addEventListener('scroll', debounce(updateIndicatorsFromScroll, 100));
    
    function createIndicators() {
        if (!indicatorsContainer) return;
        
        const visibleCards = getVisibleCards();
        const totalPages = Math.ceil(cards.length / visibleCards);
        
        for (let i = 0; i < totalPages; i++) {
            const indicator = document.createElement('div');
            indicator.className = `indicator ${i === 0 ? 'active' : ''}`;
            indicator.addEventListener('click', () => {
                currentIndex = i * visibleCards;
                updateCarousel();
            });
            indicatorsContainer.appendChild(indicator);
        }
    }
    
    function getVisibleCards() {
        const containerWidth = carousel.offsetWidth;
        return Math.floor(containerWidth / cardWidth) || 1;
    }
    
    function updateCarousel() {
        const scrollPosition = currentIndex * cardWidth;
        carousel.scrollTo({
            left: scrollPosition,
            behavior: 'smooth'
        });
        updateIndicators();
    }
    
    function updateIndicators() {
        const indicators = indicatorsContainer.querySelectorAll('.indicator');
        const visibleCards = getVisibleCards();
        const activeIndicator = Math.floor(currentIndex / visibleCards);
        
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === activeIndicator);
        });
    }
    
    function updateIndicatorsFromScroll() {
        const scrollPosition = carousel.scrollLeft;
        const newIndex = Math.round(scrollPosition / cardWidth);
        if (newIndex !== currentIndex) {
            currentIndex = newIndex;
            updateIndicators();
        }
    }
    
    function autoScroll() {
        const maxIndex = cards.length - getVisibleCards();
        if (currentIndex >= maxIndex) {
            currentIndex = 0;
        } else {
            currentIndex++;
        }
        updateCarousel();
    }
    
    // Handle window resize
    window.addEventListener('resize', debounce(() => {
        indicatorsContainer.innerHTML = '';
        createIndicators();
        currentIndex = 0;
        updateCarousel();
    }, 250));
}

// Function to load Booksy reviews dynamically (future implementation)
function loadBooksyReviews() {
    // This function will fetch real reviews from Booksy API
    // For now, it returns the static reviews we have
    
    const additionalReviews = [
        {
            author: "Miguel S.",
            text: "Excelente servicio",
            service: "Corte caballero",
            date: "Nov. 2025",
            rating: 5
        },
        {
            author: "Carlos R.",
            text: "TOP 10💪💪",
            service: "Corte y barba",
            date: "Nov. 2025",
            rating: 5
        },
        {
            author: "Antonio L.",
            text: "Es un máquina",
            service: "Corte caballero",
            date: "Oct. 2025",
            rating: 5
        }
    ];
    
    return additionalReviews;
}

function addReviewToCarousel(review) {
    const carousel = document.getElementById('reviews-carousel');
    if (!carousel) return;
    
    const reviewCard = document.createElement('div');
    reviewCard.className = 'review-card';
    
    const stars = Array(review.rating).fill('<i class="fas fa-star"></i>').join('');
    
    reviewCard.innerHTML = `
        <div class="stars">
            ${stars}
        </div>
        <p>"${review.text}"</p>
        <div class="reviewer">
            <h4>${review.author}</h4>
            <small>${review.service} • ${review.date}</small>
        </div>
    `;
    
    carousel.appendChild(reviewCard);
}

// Auto-update reviews from Booksy (placeholder)
function autoUpdateReviews() {
    // This would periodically check for new reviews
    setInterval(() => {
        const newReviews = loadBooksyReviews();
        // In a real implementation, this would add only new reviews
        console.log('Checking for new Booksy reviews...');
    }, 300000); // Check every 5 minutes
}

// Business Hours Functionality
function initBusinessHours() {
    const scheduleDays = document.querySelectorAll('.schedule-day');
    const today = new Date().getDay(); // 0 = Sunday, 1 = Monday, etc.
    
    // Map day numbers to schedule day elements
    const dayMapping = {
        1: 0, // Monday
        2: 1, // Tuesday
        3: 2, // Wednesday
        4: 3, // Thursday
        5: 4, // Friday
        6: 5, // Saturday
        0: 6  // Sunday
    };
    
    // Highlight today's schedule
    if (scheduleDays.length > 0 && dayMapping.hasOwnProperty(today)) {
        const todayElement = scheduleDays[dayMapping[today]];
        if (todayElement) {
            todayElement.style.background = 'rgba(0, 0, 0, 0.1)';
            todayElement.style.border = '2px solid var(--primary-color)';
            todayElement.style.fontWeight = '600';
            
            // Add "HOY" indicator
            const daySpan = todayElement.querySelector('.day');
            if (daySpan && !daySpan.textContent.includes('(HOY)')) {
                daySpan.innerHTML += ' <span style="color: var(--primary-color); font-size: 0.8rem;">(HOY)</span>';
            }
        }
    }
}

// Contact Form Functionality
function initContactForm() {
    // This would be implemented if we had a contact form
    // For now, we'll add some interactive feedback to contact items
    const contactItems = document.querySelectorAll('.contact-item');
    
    contactItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.contact-icon');
            if (icon) {
                icon.style.transform = 'scale(1.1) rotate(5deg)';
            }
        });
        
        item.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.contact-icon');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
        });
    });
}

// Loading Animations
function initLoadingAnimations() {
    // Add loading animation to buttons
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Only add loading animation for external links
            if (this.hasAttribute('target') && this.getAttribute('target') === '_blank') {
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando...';
                this.style.pointerEvents = 'none';
                
                // Reset after 2 seconds (simulated loading)
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.pointerEvents = 'auto';
                }, 2000);
            }
        });
    });
}

// Utility Functions
function throttle(func, wait) {
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

// Performance optimizations
const optimizedScrollHandler = throttle(initNavbarScrollEffect, 16);

// Additional Interactive Features
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to service cards
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-10px) scale(1)';
        });
    });
    
    // Add parallax effect to hero section
    const hero = document.querySelector('.hero');
    if (hero) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            hero.style.transform = `translateY(${rate}px)`;
        });
    }
    
    // Add typing effect to hero title (optional)
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';
        heroTitle.style.borderRight = '3px solid #ffffff';
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                heroTitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            } else {
                heroTitle.style.borderRight = 'none';
            }
        };
        
        setTimeout(typeWriter, 1000);
    }
});

// Error handling
window.addEventListener('error', function(e) {
    console.log('An error occurred:', e.error);
});

// Back to Top Button
function initBackToTop() {
    const backToTop = document.getElementById('backToTop');
    
    if (!backToTop) return;
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTop.classList.add('show');
        } else {
            backToTop.classList.remove('show');
        }
    });
    
    // Scroll to top on click
    backToTop.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Advanced Interactions
function initAdvancedInteractions() {
    // Add hover lift effect to cards
    const cards = document.querySelectorAll('.service-card, .review-card');
    cards.forEach(card => {
        card.classList.add('hover-lift');
    });
    
    // Add glow effect to buttons
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
    buttons.forEach(btn => {
        btn.classList.add('hover-glow');
    });
    
    // Smooth number counting animation
    initNumberCounting();
    
    // Add typing effect to hero subtitle if exists
    const heroSubtitle = document.querySelector('.hero p');
    if (heroSubtitle) {
        addTypingCursor(heroSubtitle);
    }
}

// Number Counting Animation
function initNumberCounting() {
    const stats = document.querySelectorAll('[data-count]');
    
    const observerOptions = {
        threshold: 0.5
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const targetNumber = parseInt(target.getAttribute('data-count'));
                const duration = 2000;
                const increment = targetNumber / (duration / 16);
                let current = 0;
                
                const updateCount = () => {
                    current += increment;
                    if (current < targetNumber) {
                        target.textContent = Math.floor(current);
                        requestAnimationFrame(updateCount);
                    } else {
                        target.textContent = targetNumber;
                    }
                };
                
                updateCount();
                observer.unobserve(target);
            }
        });
    }, observerOptions);
    
    stats.forEach(stat => observer.observe(stat));
}

// Add typing cursor effect
function addTypingCursor(element) {
    element.style.borderRight = '2px solid white';
    element.style.paddingRight = '5px';
    element.style.animation = 'blink 1s infinite';
}

// Service Worker Registration (for PWA capabilities)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed');
            });
    });
}