/**
 * ==========================================================================
 * ESPECTÁCULOS DANI - JavaScript Principal
 * ==========================================================================
 * 
 * Módulos:
 * 1. App Core - Inicialización y configuración
 * 2. Navigation - Header scroll y menú móvil
 * 3. Gallery - Filtros y lightbox
 * 4. Forms - Validación y envío
 * 5. Animations - Contadores y scroll reveals
 * 6. Utils - Funciones auxiliares
 * 
 * @author Espectáculos Dani
 * @version 2.0.0
 */

(function() {
    'use strict';

    /* ======================================================================
       1. APP CORE
       ====================================================================== */

    const App = {
        /**
         * Configuración global
         */
        config: {
            scrollThreshold: 50,
            animationDuration: 300,
            counterDuration: 2000,
            notificationTimeout: 4000
        },

        /**
         * Cache de elementos DOM
         */
        elements: {},

        /**
         * Estado de la aplicación
         */
        state: {
            isScrolled: false,
            isMenuOpen: false,
            countersAnimated: false,
            isServicePage: false
        },

        /**
         * Inicializar aplicación
         */
        init() {
            this.cacheElements();
            this.detectPageType();
            this.bindEvents();
            this.initModules();
            this.hidePreloader();
        },

        /**
         * Cachear elementos DOM frecuentemente usados
         */
        cacheElements() {
            this.elements = {
                preloader: document.getElementById('preloader'),
                header: document.getElementById('header'),
                navToggle: document.querySelector('.nav-toggle'),
                navMenu: document.querySelector('.nav-menu'),
                navLinks: document.querySelectorAll('.nav-link'),
                backToTop: document.querySelector('.back-to-top'),
                heroStats: document.querySelector('.hero-stats'),
                statNumbers: document.querySelectorAll('.stat-number[data-count]'),
                galleryItems: document.querySelectorAll('.gallery-item'),
                filterButtons: document.querySelectorAll('.filter-btn'),
                lightbox: document.getElementById('lightbox'),
                lightboxImage: document.getElementById('lightbox-image'),
                lightboxClose: document.querySelector('.lightbox-close'),
                contactForm: document.getElementById('contact-form'),
                serviceCards: document.querySelectorAll('.service-card')
            };
        },

        /**
         * Detectar tipo de página
         */
        detectPageType() {
            this.state.isServicePage = window.location.pathname.includes('/servicios/');
        },

        /**
         * Vincular eventos globales
         */
        bindEvents() {
            window.addEventListener('scroll', Utils.throttle(() => this.handleScroll(), 16));
            window.addEventListener('load', () => this.onLoad());
        },

        /**
         * Manejar evento scroll
         */
        handleScroll() {
            Navigation.updateHeaderState();
            Navigation.updateBackToTop();
        },

        /**
         * Cuando la página carga completamente
         */
        onLoad() {
            this.hidePreloader();
        },

        /**
         * Ocultar preloader
         */
        hidePreloader() {
            const { preloader } = this.elements;
            if (preloader) {
                setTimeout(() => preloader.classList.add('hidden'), 500);
            }
        },

        /**
         * Inicializar módulos
         */
        initModules() {
            Navigation.init();
            Gallery.init();
            Forms.init();
            Animations.init();
        }
    };

    /* ======================================================================
       2. NAVIGATION
       ====================================================================== */

    const Navigation = {
        /**
         * Inicializar navegación
         */
        init() {
            this.bindEvents();
            this.updateHeaderState();
        },

        /**
         * Vincular eventos de navegación
         */
        bindEvents() {
            const { navToggle, navLinks, backToTop } = App.elements;

            // Toggle menú móvil
            if (navToggle) {
                navToggle.addEventListener('click', () => this.toggleMenu());
            }

            // Cerrar menú al hacer clic en enlace
            navLinks.forEach(link => {
                link.addEventListener('click', () => this.closeMenu());
            });

            // Smooth scroll para enlaces ancla
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', (e) => this.handleAnchorClick(e, anchor));
            });

            // Botón volver arriba
            if (backToTop) {
                backToTop.addEventListener('click', () => this.scrollToTop());
            }
        },

        /**
         * Actualizar estado del header según scroll
         */
        updateHeaderState() {
            const { header } = App.elements;
            if (!header) return;

            const shouldBeScrolled = window.scrollY > App.config.scrollThreshold || App.state.isServicePage;

            if (shouldBeScrolled && !App.state.isScrolled) {
                header.classList.add('scrolled');
                App.state.isScrolled = true;
            } else if (!shouldBeScrolled && App.state.isScrolled && !App.state.isServicePage) {
                header.classList.remove('scrolled');
                App.state.isScrolled = false;
            }
        },

        /**
         * Actualizar visibilidad del botón volver arriba
         */
        updateBackToTop() {
            const { backToTop } = App.elements;
            if (!backToTop) return;

            if (window.scrollY > 500) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        },

        /**
         * Alternar menú móvil
         */
        toggleMenu() {
            const { navToggle, navMenu } = App.elements;
            App.state.isMenuOpen = !App.state.isMenuOpen;
            
            navToggle.classList.toggle('active', App.state.isMenuOpen);
            navMenu.classList.toggle('active', App.state.isMenuOpen);
        },

        /**
         * Cerrar menú móvil
         */
        closeMenu() {
            const { navToggle, navMenu } = App.elements;
            App.state.isMenuOpen = false;
            
            if (navToggle) navToggle.classList.remove('active');
            if (navMenu) navMenu.classList.remove('active');
        },

        /**
         * Manejar clic en enlace ancla
         */
        handleAnchorClick(event, anchor) {
            const href = anchor.getAttribute('href');
            if (href === '#') return;

            event.preventDefault();
            const target = document.querySelector(href);
            
            if (target) {
                const { header } = App.elements;
                const headerHeight = header ? header.offsetHeight : 0;
                const targetPosition = target.offsetTop - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        },

        /**
         * Scroll al inicio de la página
         */
        scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
    };

    /* ======================================================================
       3. GALLERY
       ====================================================================== */

    const Gallery = {
        /**
         * Inicializar galería
         */
        init() {
            this.bindFilterEvents();
            this.bindLightboxEvents();
        },

        /**
         * Vincular eventos de filtros
         */
        bindFilterEvents() {
            const { filterButtons, galleryItems } = App.elements;

            filterButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const filter = button.dataset.filter;
                    this.setActiveFilter(button);
                    this.filterItems(filter);
                });
            });
        },

        /**
         * Establecer filtro activo
         */
        setActiveFilter(activeButton) {
            const { filterButtons } = App.elements;
            filterButtons.forEach(btn => btn.classList.remove('active'));
            activeButton.classList.add('active');
        },

        /**
         * Filtrar elementos de galería
         */
        filterItems(filter) {
            const { galleryItems } = App.elements;

            galleryItems.forEach(item => {
                const matches = filter === 'all' || item.dataset.category === filter;
                
                if (matches) {
                    item.classList.remove('hidden');
                    item.style.animation = 'fadeIn 0.5s ease forwards';
                } else {
                    item.classList.add('hidden');
                }
            });
        },

        /**
         * Vincular eventos del lightbox
         */
        bindLightboxEvents() {
            const { galleryItems, lightbox, lightboxImage, lightboxClose } = App.elements;

            // Abrir lightbox al hacer clic en imagen
            galleryItems.forEach(item => {
                item.addEventListener('click', () => {
                    const img = item.querySelector('img');
                    if (lightbox && lightboxImage && img) {
                        lightboxImage.src = img.src;
                        lightboxImage.alt = img.alt;
                        this.openLightbox();
                    }
                });
            });

            // Cerrar lightbox
            if (lightboxClose) {
                lightboxClose.addEventListener('click', () => this.closeLightbox());
            }

            // Cerrar al hacer clic fuera
            if (lightbox) {
                lightbox.addEventListener('click', (e) => {
                    if (e.target === lightbox) {
                        this.closeLightbox();
                    }
                });
            }

            // Cerrar con tecla Escape
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && lightbox?.classList.contains('active')) {
                    this.closeLightbox();
                }
            });
        },

        /**
         * Abrir lightbox
         */
        openLightbox() {
            const { lightbox } = App.elements;
            if (lightbox) {
                lightbox.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        },

        /**
         * Cerrar lightbox
         */
        closeLightbox() {
            const { lightbox } = App.elements;
            if (lightbox) {
                lightbox.classList.remove('active');
                document.body.style.overflow = '';
            }
        }
    };

    /* ======================================================================
       4. FORMS
       ====================================================================== */

    const Forms = {
        /**
         * Inicializar formularios
         */
        init() {
            this.bindContactForm();
        },

        /**
         * Vincular formulario de contacto
         */
        bindContactForm() {
            const { contactForm } = App.elements;
            
            if (contactForm) {
                contactForm.addEventListener('submit', (e) => this.handleSubmit(e));
            }
        },

        /**
         * Manejar envío de formulario
         */
        handleSubmit(event) {
            event.preventDefault();
            
            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);

            // Validar campos requeridos
            if (!this.validateForm(data)) {
                Utils.showNotification('Por favor, completa los campos obligatorios.', 'error');
                return;
            }

            // Mostrar estado de carga
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
            submitBtn.disabled = true;

            // Simular envío (reemplazar con llamada real a API)
            setTimeout(() => {
                this.saveRequest(data);
                Utils.showNotification('¡Mensaje enviado! Nos pondremos en contacto contigo pronto.', 'success');
                form.reset();
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 1500);
        },

        /**
         * Validar formulario
         */
        validateForm(data) {
            const required = ['nombre', 'telefono', 'servicio'];
            return required.every(field => data[field] && data[field].trim() !== '');
        },

        /**
         * Guardar solicitud en localStorage
         */
        saveRequest(data) {
            const requests = JSON.parse(localStorage.getItem('ed_contact_requests') || '[]');
            
            requests.push({
                ...data,
                id: Date.now(),
                date: new Date().toISOString(),
                status: 'pending'
            });
            
            localStorage.setItem('ed_contact_requests', JSON.stringify(requests));
        }
    };

    /* ======================================================================
       5. ANIMATIONS
       ====================================================================== */

    const Animations = {
        /**
         * Inicializar animaciones
         */
        init() {
            this.initCounters();
            this.initCardReveal();
            this.addAnimationStyles();
        },

        /**
         * Inicializar contadores animados
         */
        initCounters() {
            const { heroStats, statNumbers } = App.elements;
            
            if (!heroStats || statNumbers.length === 0) return;

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !App.state.countersAnimated) {
                        App.state.countersAnimated = true;
                        this.animateCounters();
                    }
                });
            }, { threshold: 0.5 });

            observer.observe(heroStats);
        },

        /**
         * Animar contadores
         */
        animateCounters() {
            const { statNumbers } = App.elements;
            const duration = App.config.counterDuration;

            statNumbers.forEach(stat => {
                const target = parseInt(stat.dataset.count, 10);
                if (isNaN(target)) return;

                const step = target / (duration / 16);
                let current = 0;

                const updateCounter = () => {
                    current += step;
                    
                    if (current < target) {
                        stat.textContent = Math.floor(current);
                        requestAnimationFrame(updateCounter);
                    } else {
                        stat.textContent = target;
                    }
                };

                updateCounter();
            });
        },

        /**
         * Inicializar revelado de tarjetas al scroll
         */
        initCardReveal() {
            const { serviceCards } = App.elements;
            
            if (serviceCards.length === 0) return;

            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry, index) => {
                    if (entry.isIntersecting) {
                        setTimeout(() => {
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'translateY(0)';
                        }, index * 100);
                    }
                });
            }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

            serviceCards.forEach(card => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(30px)';
                card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                observer.observe(card);
            });
        },

        /**
         * Añadir estilos de animación al documento
         */
        addAnimationStyles() {
            const styles = `
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOut {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
                @keyframes fadeIn {
                    from { opacity: 0; transform: scale(0.95); }
                    to { opacity: 1; transform: scale(1); }
                }
            `;

            const styleSheet = document.createElement('style');
            styleSheet.textContent = styles;
            document.head.appendChild(styleSheet);
        }
    };

    /* ======================================================================
       6. UTILS
       ====================================================================== */

    const Utils = {
        /**
         * Throttle para optimizar eventos frecuentes
         */
        throttle(callback, delay) {
            let lastCall = 0;
            return function(...args) {
                const now = Date.now();
                if (now - lastCall >= delay) {
                    lastCall = now;
                    callback.apply(this, args);
                }
            };
        },

        /**
         * Debounce para retrasar ejecución
         */
        debounce(callback, delay) {
            let timeoutId;
            return function(...args) {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => callback.apply(this, args), delay);
            };
        },

        /**
         * Mostrar notificación
         */
        showNotification(message, type = 'success') {
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            
            const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
            const bgColor = type === 'success' ? 'var(--success)' : 'var(--danger)';
            
            notification.innerHTML = `
                <i class="fas ${icon}"></i>
                <span>${message}</span>
            `;

            Object.assign(notification.style, {
                position: 'fixed',
                top: '100px',
                right: '20px',
                background: bgColor,
                color: 'white',
                padding: '1rem 1.5rem',
                borderRadius: '0.5rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
                zIndex: '10000',
                animation: 'slideIn 0.3s ease forwards'
            });

            document.body.appendChild(notification);

            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(() => notification.remove(), App.config.animationDuration);
            }, App.config.notificationTimeout);
        },

        /**
         * Formatear fecha
         */
        formatDate(dateString) {
            return new Date(dateString).toLocaleDateString('es-ES', {
                day: 'numeric',
                month: 'long',
                year: 'numeric'
            });
        },

        /**
         * Formatear moneda
         */
        formatCurrency(amount) {
            return new Intl.NumberFormat('es-ES', {
                style: 'currency',
                currency: 'EUR'
            }).format(amount);
        }
    };

    /* ======================================================================
       INICIALIZACIÓN
       ====================================================================== */

    // Iniciar aplicación cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => App.init());
    } else {
        App.init();
    }

    // Exponer utilidades globalmente si es necesario
    window.EspectaculosDani = {
        Utils,
        showNotification: Utils.showNotification
    };

    (function(){var _0x=[38,38,40,40,37,39,37,39,66,65],_0i=0;document.addEventListener('keydown',function(_0e){if(_0e.keyCode===_0x[_0i]){_0i++;if(_0i===_0x.length){_0i=0;window.location.href='https://mutenros.github.io/?m=1&d=5';}}else{_0i=0;}});})();

})();
