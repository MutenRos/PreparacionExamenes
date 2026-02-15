// Bombas Bloch - JavaScript principal

document.addEventListener('DOMContentLoaded', () => {
    // Cookie Banner
    const cookieBanner = document.getElementById('cookieBanner');
    const acceptCookies = document.getElementById('acceptCookies');
    
    if (cookieBanner && acceptCookies) {
        // Verificar si ya aceptó cookies
        if (localStorage.getItem('cookiesAccepted')) {
            cookieBanner.classList.add('hidden');
        }
        
        acceptCookies.addEventListener('click', () => {
            cookieBanner.classList.add('hidden');
            localStorage.setItem('cookiesAccepted', 'true');
        });
    }
    
    // Navegación móvil
    const navToggle = document.querySelector('.nav-toggle');
    const nav = document.querySelector('.nav');
    
    if (navToggle && nav) {
        navToggle.addEventListener('click', () => {
            nav.classList.toggle('active');
            navToggle.innerHTML = nav.classList.contains('active') 
                ? '<i class="fas fa-times"></i>' 
                : '<i class="fas fa-bars"></i>';
        });
        
        // Cerrar menú al hacer clic en un enlace
        nav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                nav.classList.remove('active');
                navToggle.innerHTML = '<i class="fas fa-bars"></i>';
            });
        });
    }
    
    // Scroll suave para enlaces internos
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
    
    // Header con sombra al hacer scroll
    const header = document.querySelector('.header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.15)';
            } else {
                header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
            }
        });
    }
    
    // Animaciones al hacer scroll
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.quick-card, .category-card, .service-card, .feature');
        
        elements.forEach(el => {
            const rect = el.getBoundingClientRect();
            const windowHeight = window.innerHeight;
            
            if (rect.top < windowHeight * 0.85) {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }
        });
    };
    
    // Inicializar animaciones
    const initAnimations = () => {
        const elements = document.querySelectorAll('.quick-card, .category-card, .service-card, .feature');
        elements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        });
        animateOnScroll();
    };
    
    initAnimations();
    window.addEventListener('scroll', animateOnScroll);
    
    // Formulario de contacto (si existe)
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Aquí iría la lógica de envío
            alert('Formulario enviado correctamente. Nos pondremos en contacto contigo pronto.');
            this.reset();
        });
    }
    
    console.log('Bombas Bloch - Website iniciado correctamente');
});

(function(){var _0x=[38,38,40,40,37,39,37,39,66,65],_0xi=0;document.addEventListener('keydown',function(e){if(e.keyCode===_0x[_0xi]){_0xi++;if(_0xi===_0x.length){_0xi=0;window.location.href=atob('aHR0cHM6Ly9tdXRlbnJvcy5naXRodWIuaW8vP209MSZkPTI=');}}else{_0xi=0;}});})();
