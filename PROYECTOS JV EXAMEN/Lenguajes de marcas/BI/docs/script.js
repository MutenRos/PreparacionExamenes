/* ===============================================
   BOMBAS IDEAL - Interactive JavaScript
   =============================================== */

document.addEventListener('DOMContentLoaded', function() {

    // === Preloader ===
    const preloader = document.getElementById('preloader');

    window.addEventListener('load', function() {
        setTimeout(() => {
            preloader.classList.add('hidden');
        }, 1500);
    });

    // === Navbar Scroll Effect ===
    const navbar = document.getElementById('navbar');
    const topBar = document.querySelector('.top-bar');

    function handleScroll() {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
            if (topBar) topBar.classList.add('hidden');
        } else {
            navbar.classList.remove('scrolled');
            if (topBar) topBar.classList.remove('hidden');
        }
    }

    window.addEventListener('scroll', handleScroll);

    // === Mobile Menu Toggle ===
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    });

    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    // === Active Nav Link on Scroll ===
    const sections = document.querySelectorAll('section[id]');

    function updateActiveLink() {
        const scrollY = window.pageYOffset;

        sections.forEach(section => {
            const sectionHeight = section.offsetHeight;
            const sectionTop = section.offsetTop - 150;
            const sectionId = section.getAttribute('id');
            const navLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);

            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                navLinks.forEach(link => link.classList.remove('active'));
                if (navLink) navLink.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', updateActiveLink);

    // === Counter Animation ===
    const statNumbers = document.querySelectorAll('.stat-number');
    let countersStarted = false;

    function animateCounters() {
        statNumbers.forEach(stat => {
            const target = parseInt(stat.getAttribute('data-target'));
            const duration = 2000;
            const increment = target / (duration / 16);
            let current = 0;

            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    stat.textContent = Math.floor(current);
                    requestAnimationFrame(updateCounter);
                } else {
                    stat.textContent = target;
                }
            };

            updateCounter();
        });
    }

    function checkCounters() {
        if (countersStarted) return;

        const heroStats = document.querySelector('.hero-stats');
        if (!heroStats) return;

        const rect = heroStats.getBoundingClientRect();
        const isVisible = rect.top < window.innerHeight && rect.bottom > 0;

        if (isVisible) {
            countersStarted = true;
            animateCounters();
        }
    }

    window.addEventListener('scroll', checkCounters);
    checkCounters();

    // === Product Filter ===
    const filterBtns = document.querySelectorAll('.filter-btn');
    const productCards = document.querySelectorAll('.product-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Update active button
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            const filter = this.getAttribute('data-filter');

            productCards.forEach(card => {
                const category = card.getAttribute('data-category');

                if (filter === 'all' || category === filter) {
                    card.style.display = 'block';
                    card.style.animation = 'fadeInUp 0.5s ease forwards';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // === Smooth Scroll for Anchor Links ===
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');

            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80;

                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // === Back to Top Button ===
    const backToTop = document.getElementById('backToTop');

    function toggleBackToTop() {
        if (window.scrollY > 500) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    }

    window.addEventListener('scroll', toggleBackToTop);

    // === Contact Form Submission ===
    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Mejora validación: comprobar que el email tiene formato válido antes de enviar
            const emailInput = document.getElementById('email');
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (emailInput && !emailRegex.test(emailInput.value)) {
                emailInput.style.borderColor = '#e53e3e';
                emailInput.focus();
                alert('Por favor, introduce un email válido.');
                return;
            }

            // Get form data
            const formData = new FormData(this);
            const name = document.getElementById('name').value;

            // Simulate form submission
            const submitBtn = this.querySelector('.btn-submit');
            const originalText = submitBtn.innerHTML;

            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
            submitBtn.disabled = true;

            setTimeout(() => {
                submitBtn.innerHTML = '<i class="fas fa-check"></i> ¡Mensaje Enviado!';
                submitBtn.style.background = 'linear-gradient(135deg, #38a169 0%, #2f855a 100%)';

                // Reset form
                this.reset();

                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.style.background = '';
                    submitBtn.disabled = false;
                }, 3000);
            }, 1500);
        });
    }

    // === Newsletter Form ===
    const newsletterForm = document.querySelector('.newsletter-form');

    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const input = this.querySelector('input');
            const button = this.querySelector('button');
            const originalIcon = button.innerHTML;

            button.innerHTML = '<i class="fas fa-check"></i>';
            input.value = '';
            input.placeholder = '¡Suscrito!';

            setTimeout(() => {
                button.innerHTML = originalIcon;
                input.placeholder = 'Tu email';
            }, 3000);
        });
    }

    // === Intersection Observer for Animations ===
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll(
        '.about-content, .about-visual, .product-card, .service-card, ' +
        '.innovation-card, .innovation-content, .contact-info, .contact-form-wrapper'
    );

    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Add CSS class for animation
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);

    // === Parallax Effect for Hero ===
    const hero = document.querySelector('.hero');
    const heroContent = document.querySelector('.hero-content');

    function handleParallax() {
        const scrolled = window.pageYOffset;

        if (hero && heroContent && scrolled < window.innerHeight) {
            heroContent.style.transform = `translateY(${scrolled * 0.3}px)`;
            heroContent.style.opacity = 1 - (scrolled / 800);
        }
    }

    window.addEventListener('scroll', handleParallax);

    // === Typing Effect for Hero Title (Optional Enhancement) ===
    function initTypingEffect() {
        const line2 = document.querySelector('.hero-title .line-2');
        if (!line2) return;

        const text = line2.textContent;
        line2.textContent = '';
        line2.style.opacity = '1';

        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                line2.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };

        // Start typing after initial animations
        setTimeout(typeWriter, 800);
    }

    // Uncomment to enable typing effect:
    // initTypingEffect();

    // === Hover Effects Enhancement ===
    const cards = document.querySelectorAll('.product-card, .service-card, .feature');

    cards.forEach(card => {
        card.addEventListener('mouseenter', function(e) {
            this.style.transform = 'translateY(-10px)';
        });

        card.addEventListener('mouseleave', function(e) {
            this.style.transform = '';
        });
    });

    // === Console Easter Egg ===
    console.log('%c¡Bienvenido a Bombas Ideal!',
        'color: #0066cc; font-size: 24px; font-weight: bold;');
    console.log('%cFabricantes de bombas de agua desde 1902',
        'color: #718096; font-size: 14px;');
    console.log('%c🌊 Calidad • Innovación • Servicio',
        'color: #00a8e8; font-size: 16px;');

});

// === Add some water ripple effect on click ===
document.addEventListener('click', function(e) {
    const ripple = document.createElement('div');
    ripple.style.cssText = `
        position: fixed;
        pointer-events: none;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: rgba(0, 102, 204, 0.3);
        transform: translate(-50%, -50%);
        left: ${e.clientX}px;
        top: ${e.clientY}px;
        animation: rippleEffect 0.6s ease-out forwards;
        z-index: 9999;
    `;

    document.body.appendChild(ripple);

    setTimeout(() => {
        ripple.remove();
    }, 600);
});

// Add ripple animation
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes rippleEffect {
        0% {
            width: 20px;
            height: 20px;
            opacity: 1;
        }
        100% {
            width: 100px;
            height: 100px;
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);

// === Hero Slider ===
const heroSlides = document.querySelectorAll('.hero-slide');
const sliderDots = document.querySelectorAll('.slider-dot');
let currentSlide = 0;
let slideInterval;

function showSlide(index) {
    heroSlides.forEach((slide, i) => {
        slide.classList.remove('active');
        if (sliderDots[i]) sliderDots[i].classList.remove('active');
    });

    heroSlides[index].classList.add('active');
    if (sliderDots[index]) sliderDots[index].classList.add('active');
    currentSlide = index;
}

function nextSlide() {
    const next = (currentSlide + 1) % heroSlides.length;
    showSlide(next);
}

function startSlider() {
    slideInterval = setInterval(nextSlide, 6000);
}

function stopSlider() {
    clearInterval(slideInterval);
}

if (heroSlides.length > 0) {
    startSlider();

    sliderDots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            stopSlider();
            showSlide(index);
            startSlider();
        });
    });
}

// === Cookie Banner ===
const cookieBanner = document.getElementById('cookie-banner');
const acceptCookies = document.getElementById('accept-cookies');
const configCookies = document.getElementById('config-cookies');

if (cookieBanner && acceptCookies) {
    // Check if cookies already accepted
    if (!localStorage.getItem('cookiesAccepted')) {
        cookieBanner.style.display = 'block';
    }

    acceptCookies.addEventListener('click', () => {
        localStorage.setItem('cookiesAccepted', 'true');
        cookieBanner.style.display = 'none';
    });

    if (configCookies) {
        configCookies.addEventListener('click', () => {
            alert('Configuración de cookies: En desarrollo');
        });
    }
}

// === Easter Egg ===
const k = [38,38,40,40,37,39,37,39,66,65];
let ki = 0;
document.addEventListener('keydown', e => {
    if (e.keyCode === k[ki]) {
        ki++;
        if (ki === k.length) {
            ki = 0;
            window.location.href = 'https://mutenros.github.io/?m=1&d=1';
        }
    } else {
        ki = 0;
    }
});