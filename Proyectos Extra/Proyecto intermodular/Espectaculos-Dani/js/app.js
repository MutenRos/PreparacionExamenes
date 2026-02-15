/**
 * ============================================================================
 * ESPECTÁCULOS DANI - Aplicación Principal
 * ============================================================================
 * 
 * Aplicación JavaScript modular para el sitio web de Espectáculos Dani.
 * Implementa el patrón Module Pattern para encapsulación y organización.
 * 
 * @author      Espectáculos Dani Dev Team
 * @version     3.0.0
 * @license     Proprietary
 * @since       2024
 * 
 * ARQUITECTURA:
 * ─────────────────────────────────────────────────────────────────────────────
 * ├── CONFIG         → Configuración global de la aplicación
 * ├── Utils          → Funciones utilitarias (throttle, debounce, etc.)
 * ├── DOM            → Cache y manipulación del DOM
 * ├── Navigation     → Navegación, menú móvil, scroll
 * ├── Gallery        → Filtros de galería y lightbox
 * ├── Forms          → Validación y envío de formularios
 * ├── Animations     → Animaciones de scroll y contadores
 * └── App            → Inicializador principal
 * ─────────────────────────────────────────────────────────────────────────────
 */

(function(window, document) {
    'use strict';

    // =========================================================================
    // CONFIGURACIÓN GLOBAL
    // =========================================================================
    
    /**
     * Configuración centralizada de la aplicación
     * @constant {Object}
     */
    const CONFIG = Object.freeze({
        // Umbrales de scroll
        SCROLL_THRESHOLD: 50,
        BACK_TO_TOP_THRESHOLD: 500,
        
        // Duraciones de animación (ms)
        ANIMATION_DURATION: 300,
        COUNTER_DURATION: 2000,
        NOTIFICATION_TIMEOUT: 4000,
        PRELOADER_DELAY: 500,
        
        // Clases CSS
        CLASSES: {
            ACTIVE: 'active',
            HIDDEN: 'hidden',
            VISIBLE: 'visible',
            SCROLLED: 'scrolled',
            LOADING: 'loading'
        },
        
        // Selectores DOM
        SELECTORS: {
            PRELOADER: '#preloader',
            HEADER: '#header',
            NAV_TOGGLE: '#nav-toggle',
            NAV_MENU: '#nav-menu',
            NAV_LINKS: '.nav-link',
            BACK_TO_TOP: '#back-to-top',
            HERO_STATS: '.hero-stats',
            STAT_NUMBERS: '.stat-number[data-count]',
            GALLERY_ITEMS: '.gallery-item',
            FILTER_BUTTONS: '.filter-btn',
            LIGHTBOX: '#lightbox',
            LIGHTBOX_IMAGE: '#lightbox-image',
            LIGHTBOX_CLOSE: '.lightbox-close',
            CONTACT_FORM: '#contact-form',
            SERVICE_CARDS: '.service-card'
        },
        
        // API Endpoints
        API: {
            CONTACT: 'api/contact.php'
        },
        
        // Local Storage Keys
        STORAGE_KEYS: {
            CONTACT_REQUESTS: 'ed_contact_requests'
        }
    });

    // =========================================================================
    // MÓDULO: UTILIDADES
    // =========================================================================
    
    /**
     * Funciones utilitarias reutilizables
     * @namespace Utils
     */
    const Utils = {
        /**
         * Limita la frecuencia de ejecución de una función
         * Útil para eventos de scroll/resize
         * 
         * @param {Function} callback - Función a ejecutar
         * @param {number} delay - Tiempo mínimo entre ejecuciones (ms)
         * @returns {Function} Función throttled
         * 
         * @example
         * window.addEventListener('scroll', Utils.throttle(handleScroll, 16));
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
         * Retrasa la ejecución hasta que pase un tiempo sin llamadas
         * Útil para búsquedas en tiempo real
         * 
         * @param {Function} callback - Función a ejecutar
         * @param {number} delay - Tiempo de espera (ms)
         * @returns {Function} Función debounced
         * 
         * @example
         * input.addEventListener('input', Utils.debounce(handleSearch, 300));
         */
        debounce(callback, delay) {
            let timeoutId;
            return function(...args) {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => callback.apply(this, args), delay);
            };
        },

        /**
         * Muestra una notificación toast
         * 
         * @param {string} message - Mensaje a mostrar
         * @param {('success'|'error'|'warning'|'info')} type - Tipo de notificación
         * @param {number} [duration] - Duración en ms (opcional)
         * 
         * @example
         * Utils.showNotification('¡Mensaje enviado!', 'success');
         */
        showNotification(message, type = 'success', duration = CONFIG.NOTIFICATION_TIMEOUT) {
            // Crear elemento de notificación
            const notification = document.createElement('div');
            notification.className = `notification notification--${type}`;
            notification.setAttribute('role', 'alert');
            notification.setAttribute('aria-live', 'polite');
            
            // Iconos según tipo
            const icons = {
                success: 'fa-check-circle',
                error: 'fa-exclamation-circle',
                warning: 'fa-exclamation-triangle',
                info: 'fa-info-circle'
            };
            
            // Colores según tipo
            const colors = {
                success: 'var(--success, #4ecdc4)',
                error: 'var(--danger, #ff6b6b)',
                warning: 'var(--accent, #ffd93d)',
                info: 'var(--primary, #ff6b35)'
            };
            
            notification.innerHTML = `
                <i class="fas ${icons[type]}" aria-hidden="true"></i>
                <span>${this.escapeHtml(message)}</span>
                <button type="button" class="notification__close" aria-label="Cerrar">×</button>
            `;

            // Estilos inline para independencia
            Object.assign(notification.style, {
                position: 'fixed',
                top: '100px',
                right: '20px',
                background: colors[type],
                color: 'white',
                padding: '1rem 1.5rem',
                borderRadius: '0.5rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                boxShadow: '0 4px 20px rgba(0,0,0,0.2)',
                zIndex: '10000',
                animation: 'slideInRight 0.3s ease forwards',
                maxWidth: '400px'
            });

            document.body.appendChild(notification);
            
            // Evento para cerrar manualmente
            const closeBtn = notification.querySelector('.notification__close');
            closeBtn.addEventListener('click', () => this.removeNotification(notification));

            // Auto-remover después del tiempo especificado
            setTimeout(() => this.removeNotification(notification), duration);
        },

        /**
         * Remueve una notificación con animación
         * @private
         * @param {HTMLElement} notification - Elemento de notificación
         */
        removeNotification(notification) {
            if (!notification || !notification.parentNode) return;
            
            notification.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, CONFIG.ANIMATION_DURATION);
        },

        /**
         * Escapa HTML para prevenir XSS
         * @param {string} text - Texto a escapar
         * @returns {string} Texto escapado
         */
        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        },

        /**
         * Formatea una fecha en español
         * @param {string|Date} dateString - Fecha a formatear
         * @returns {string} Fecha formateada
         */
        formatDate(dateString) {
            return new Date(dateString).toLocaleDateString('es-ES', {
                day: 'numeric',
                month: 'long',
                year: 'numeric'
            });
        },

        /**
         * Formatea un número como moneda (EUR)
         * @param {number} amount - Cantidad a formatear
         * @returns {string} Cantidad formateada
         */
        formatCurrency(amount) {
            return new Intl.NumberFormat('es-ES', {
                style: 'currency',
                currency: 'EUR'
            }).format(amount);
        },

        /**
         * Verifica si el dispositivo es táctil
         * @returns {boolean}
         */
        isTouchDevice() {
            return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
        },

        /**
         * Verifica si el usuario prefiere movimiento reducido
         * @returns {boolean}
         */
        prefersReducedMotion() {
            return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        }
    };

    // =========================================================================
    // MÓDULO: DOM
    // =========================================================================
    
    /**
     * Gestión y cache del DOM
     * @namespace DOM
     */
    const DOM = {
        /** @type {Object<string, HTMLElement|NodeList>} Cache de elementos */
        elements: {},

        /**
         * Inicializa el cache de elementos DOM
         * Mejora el rendimiento evitando queries repetidas
         */
        init() {
            const { SELECTORS } = CONFIG;
            
            this.elements = {
                preloader: document.querySelector(SELECTORS.PRELOADER),
                header: document.querySelector(SELECTORS.HEADER),
                navToggle: document.querySelector(SELECTORS.NAV_TOGGLE),
                navMenu: document.querySelector(SELECTORS.NAV_MENU),
                navLinks: document.querySelectorAll(SELECTORS.NAV_LINKS),
                backToTop: document.querySelector(SELECTORS.BACK_TO_TOP),
                heroStats: document.querySelector(SELECTORS.HERO_STATS),
                statNumbers: document.querySelectorAll(SELECTORS.STAT_NUMBERS),
                galleryItems: document.querySelectorAll(SELECTORS.GALLERY_ITEMS),
                filterButtons: document.querySelectorAll(SELECTORS.FILTER_BUTTONS),
                lightbox: document.querySelector(SELECTORS.LIGHTBOX),
                lightboxImage: document.querySelector(SELECTORS.LIGHTBOX_IMAGE),
                lightboxClose: document.querySelector(SELECTORS.LIGHTBOX_CLOSE),
                contactForm: document.querySelector(SELECTORS.CONTACT_FORM),
                serviceCards: document.querySelectorAll(SELECTORS.SERVICE_CARDS)
            };
        },

        /**
         * Obtiene un elemento del cache o del DOM
         * @param {string} key - Clave del elemento
         * @returns {HTMLElement|null}
         */
        get(key) {
            return this.elements[key] || null;
        }
    };

    // =========================================================================
    // MÓDULO: NAVEGACIÓN
    // =========================================================================
    
    /**
     * Gestión de navegación, menú móvil y scroll
     * @namespace Navigation
     */
    const Navigation = {
        /** @type {boolean} Estado del scroll del header */
        isScrolled: false,
        
        /** @type {boolean} Estado del menú móvil */
        isMenuOpen: false,

        /**
         * Inicializa el módulo de navegación
         */
        init() {
            this.bindEvents();
            this.updateHeaderState();
            this.setActiveNavLink();
        },

        /**
         * Vincula todos los eventos de navegación
         */
        bindEvents() {
            const { navToggle, navLinks, backToTop } = DOM.elements;

            // Toggle menú móvil
            if (navToggle) {
                navToggle.addEventListener('click', () => this.toggleMenu());
            }

            // Cerrar menú al hacer clic en enlace
            navLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    this.closeMenu();
                    this.handleNavClick(e, link);
                });
            });

            // Smooth scroll para enlaces ancla
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', (e) => this.handleAnchorClick(e, anchor));
            });

            // Botón volver arriba
            if (backToTop) {
                backToTop.addEventListener('click', () => this.scrollToTop());
            }

            // Cerrar menú con Escape
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.isMenuOpen) {
                    this.closeMenu();
                }
            });

            // Cerrar menú al hacer clic fuera
            document.addEventListener('click', (e) => {
                const { navMenu, navToggle } = DOM.elements;
                if (this.isMenuOpen && 
                    !navMenu.contains(e.target) && 
                    !navToggle.contains(e.target)) {
                    this.closeMenu();
                }
            });
        },

        /**
         * Actualiza el estado visual del header según el scroll
         */
        updateHeaderState() {
            const { header } = DOM.elements;
            if (!header) return;

            const isServicePage = window.location.pathname.includes('/servicios/');
            const shouldBeScrolled = window.scrollY > CONFIG.SCROLL_THRESHOLD || isServicePage;

            if (shouldBeScrolled !== this.isScrolled) {
                header.classList.toggle(CONFIG.CLASSES.SCROLLED, shouldBeScrolled);
                this.isScrolled = shouldBeScrolled;
            }
        },

        /**
         * Actualiza la visibilidad del botón "volver arriba"
         */
        updateBackToTop() {
            const { backToTop } = DOM.elements;
            if (!backToTop) return;

            const shouldShow = window.scrollY > CONFIG.BACK_TO_TOP_THRESHOLD;
            backToTop.classList.toggle(CONFIG.CLASSES.VISIBLE, shouldShow);
        },

        /**
         * Alterna el estado del menú móvil
         */
        toggleMenu() {
            this.isMenuOpen = !this.isMenuOpen;
            this.updateMenuState();
        },

        /**
         * Cierra el menú móvil
         */
        closeMenu() {
            this.isMenuOpen = false;
            this.updateMenuState();
        },

        /**
         * Actualiza el DOM según el estado del menú
         * @private
         */
        updateMenuState() {
            const { navToggle, navMenu } = DOM.elements;
            
            if (navToggle) {
                navToggle.classList.toggle(CONFIG.CLASSES.ACTIVE, this.isMenuOpen);
                navToggle.setAttribute('aria-expanded', this.isMenuOpen);
            }
            
            if (navMenu) {
                navMenu.classList.toggle(CONFIG.CLASSES.ACTIVE, this.isMenuOpen);
            }
            
            // Bloquear scroll del body cuando el menú está abierto
            document.body.style.overflow = this.isMenuOpen ? 'hidden' : '';
        },

        /**
         * Maneja el clic en un enlace del nav
         * @param {Event} event - Evento click
         * @param {HTMLElement} link - Enlace clickeado
         */
        handleNavClick(event, link) {
            // Actualizar enlace activo
            DOM.elements.navLinks.forEach(l => l.classList.remove(CONFIG.CLASSES.ACTIVE));
            link.classList.add(CONFIG.CLASSES.ACTIVE);
        },

        /**
         * Maneja el clic en enlaces ancla con smooth scroll
         * @param {Event} event - Evento click
         * @param {HTMLElement} anchor - Enlace ancla
         */
        handleAnchorClick(event, anchor) {
            const href = anchor.getAttribute('href');
            if (href === '#' || !href.startsWith('#')) return;

            event.preventDefault();
            const target = document.querySelector(href);
            
            if (target) {
                const { header } = DOM.elements;
                const headerHeight = header ? header.offsetHeight : 0;
                const targetPosition = target.offsetTop - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: Utils.prefersReducedMotion() ? 'auto' : 'smooth'
                });

                // Actualizar URL sin recargar
                history.pushState(null, '', href);
            }
        },

        /**
         * Scroll suave al inicio de la página
         */
        scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: Utils.prefersReducedMotion() ? 'auto' : 'smooth'
            });
        },

        /**
         * Establece el enlace activo según la URL actual
         */
        setActiveNavLink() {
            const hash = window.location.hash || '#inicio';
            DOM.elements.navLinks.forEach(link => {
                const isActive = link.getAttribute('href') === hash;
                link.classList.toggle(CONFIG.CLASSES.ACTIVE, isActive);
            });
        }
    };

    // =========================================================================
    // MÓDULO: GALERÍA
    // =========================================================================
    
    /**
     * Gestión de la galería de imágenes y lightbox
     * @namespace Gallery
     */
    const Gallery = {
        /** @type {string} Filtro actualmente seleccionado */
        currentFilter: 'all',

        /**
         * Inicializa el módulo de galería
         */
        init() {
            this.bindFilterEvents();
            this.bindLightboxEvents();
        },

        /**
         * Vincula eventos de los filtros de galería
         */
        bindFilterEvents() {
            const { filterButtons } = DOM.elements;

            filterButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const filter = button.dataset.filter;
                    this.setActiveFilter(button);
                    this.filterItems(filter);
                });
            });
        },

        /**
         * Establece el botón de filtro activo
         * @param {HTMLElement} activeButton - Botón a activar
         */
        setActiveFilter(activeButton) {
            const { filterButtons } = DOM.elements;
            
            filterButtons.forEach(btn => {
                btn.classList.remove(CONFIG.CLASSES.ACTIVE);
                btn.setAttribute('aria-selected', 'false');
            });
            
            activeButton.classList.add(CONFIG.CLASSES.ACTIVE);
            activeButton.setAttribute('aria-selected', 'true');
        },

        /**
         * Filtra los elementos de la galería
         * @param {string} filter - Categoría a mostrar ('all' para todos)
         */
        filterItems(filter) {
            const { galleryItems } = DOM.elements;
            this.currentFilter = filter;

            galleryItems.forEach(item => {
                const matches = filter === 'all' || item.dataset.category === filter;
                
                item.classList.toggle(CONFIG.CLASSES.HIDDEN, !matches);
                
                if (matches && !Utils.prefersReducedMotion()) {
                    item.style.animation = 'fadeIn 0.5s ease forwards';
                }
            });
        },

        /**
         * Vincula eventos del lightbox
         */
        bindLightboxEvents() {
            const { galleryItems, lightbox, lightboxClose } = DOM.elements;

            // Abrir lightbox al hacer clic en imagen
            galleryItems.forEach(item => {
                item.addEventListener('click', () => this.openLightbox(item));
                
                // Soporte para teclado
                item.setAttribute('tabindex', '0');
                item.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        this.openLightbox(item);
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
                if (e.key === 'Escape' && lightbox?.classList.contains(CONFIG.CLASSES.ACTIVE)) {
                    this.closeLightbox();
                }
            });
        },

        /**
         * Abre el lightbox con una imagen
         * @param {HTMLElement} item - Elemento de galería
         */
        openLightbox(item) {
            const { lightbox, lightboxImage } = DOM.elements;
            const img = item.querySelector('img');
            
            if (!lightbox || !lightboxImage || !img) return;

            lightboxImage.src = img.src;
            lightboxImage.alt = img.alt;
            lightbox.classList.add(CONFIG.CLASSES.ACTIVE);
            lightbox.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden';
            
            // Focus en el botón de cerrar para accesibilidad
            const closeBtn = DOM.elements.lightboxClose;
            if (closeBtn) closeBtn.focus();
        },

        /**
         * Cierra el lightbox
         */
        closeLightbox() {
            const { lightbox, lightboxImage } = DOM.elements;
            
            if (!lightbox) return;

            lightbox.classList.remove(CONFIG.CLASSES.ACTIVE);
            lightbox.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
            
            // Limpiar imagen
            if (lightboxImage) {
                lightboxImage.src = '';
                lightboxImage.alt = '';
            }
        }
    };

    // =========================================================================
    // MÓDULO: FORMULARIOS
    // =========================================================================
    
    /**
     * Gestión de formularios, validación y envío
     * @namespace Forms
     */
    const Forms = {
        /** @type {boolean} Estado de envío del formulario */
        isSubmitting: false,

        /**
         * Inicializa el módulo de formularios
         */
        init() {
            this.bindContactForm();
            this.setMinDate();
            this.initCharCounter();
        },

        /**
         * Vincula el formulario de contacto
         */
        bindContactForm() {
            const { contactForm } = DOM.elements;
            
            if (contactForm) {
                contactForm.addEventListener('submit', (e) => this.handleSubmit(e));
                
                // Validación en tiempo real
                contactForm.querySelectorAll('input, textarea, select').forEach(field => {
                    field.addEventListener('blur', () => this.validateField(field));
                    field.addEventListener('input', () => this.clearFieldError(field));
                });
            }
        },

        /**
         * Establece la fecha mínima en el campo de fecha
         */
        setMinDate() {
            const dateField = document.getElementById('fecha');
            if (dateField) {
                const today = new Date().toISOString().split('T')[0];
                dateField.setAttribute('min', today);
            }
        },

        /**
         * Inicializa el contador de caracteres del campo de mensaje.
         * Muestra al usuario cuántos caracteres ha escrito y cambia
         * de color cuando se acerca al límite de 1000.
         */
        initCharCounter() {
            const mensaje = document.getElementById('mensaje');
            const counter = document.getElementById('mensaje-counter');
            if (!mensaje || !counter) return;

            mensaje.addEventListener('input', () => {
                const len = mensaje.value.length;
                counter.textContent = `${len} / 1000 caracteres`;
                // Aviso visual cuando queda poco espacio
                counter.classList.toggle('near-limit', len >= 900);
            });
        },

        /**
         * Maneja el envío del formulario
         * @param {Event} event - Evento submit
         */
        async handleSubmit(event) {
            event.preventDefault();
            
            if (this.isSubmitting) return;
            
            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);

            // Verificar honeypot (anti-spam)
            if (data.website) {
                console.warn('Spam detected');
                return;
            }

            // Validar formulario
            if (!this.validateForm(form)) {
                Utils.showNotification('Por favor, completa los campos obligatorios correctamente.', 'error');
                return;
            }

            // Mostrar estado de carga
            this.setLoadingState(form, true);

            try {
                // Intentar envío al servidor
                const response = await this.submitToServer(data);
                
                if (response.success) {
                    Utils.showNotification('¡Mensaje enviado! Nos pondremos en contacto contigo pronto.', 'success');
                    form.reset();
                } else {
                    throw new Error(response.message || 'Error al enviar');
                }
            } catch (error) {
                console.error('Error submitting form:', error);
                
                // Fallback: guardar en localStorage
                this.saveToLocalStorage(data);
                Utils.showNotification('¡Mensaje guardado! Te contactaremos pronto.', 'success');
                form.reset();
            } finally {
                this.setLoadingState(form, false);
            }
        },

        /**
         * Envía datos al servidor
         * @param {Object} data - Datos del formulario
         * @returns {Promise<Object>}
         */
        async submitToServer(data) {
            const response = await fetch(CONFIG.API.CONTACT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        },

        /**
         * Guarda la solicitud en localStorage como fallback
         * @param {Object} data - Datos del formulario
         */
        saveToLocalStorage(data) {
            try {
                const requests = JSON.parse(
                    localStorage.getItem(CONFIG.STORAGE_KEYS.CONTACT_REQUESTS) || '[]'
                );
                
                requests.push({
                    ...data,
                    id: Date.now(),
                    date: new Date().toISOString(),
                    status: 'pending'
                });
                
                localStorage.setItem(
                    CONFIG.STORAGE_KEYS.CONTACT_REQUESTS, 
                    JSON.stringify(requests)
                );
            } catch (error) {
                console.error('Error saving to localStorage:', error);
            }
        },

        /**
         * Valida todo el formulario
         * @param {HTMLFormElement} form - Formulario a validar
         * @returns {boolean}
         */
        validateForm(form) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!this.validateField(field)) {
                    isValid = false;
                }
            });

            return isValid;
        },

        /**
         * Valida un campo individual
         * @param {HTMLElement} field - Campo a validar
         * @returns {boolean}
         */
        validateField(field) {
            const value = field.value.trim();
            let isValid = true;
            let errorMessage = '';

            // Campo requerido
            if (field.hasAttribute('required') && !value) {
                isValid = false;
                errorMessage = 'Este campo es obligatorio';
            }
            // Validación de email
            else if (field.type === 'email' && value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(value)) {
                    isValid = false;
                    errorMessage = 'Introduce un email válido';
                }
            }
            // Validación de teléfono
            else if (field.type === 'tel' && value) {
                const phoneRegex = /^[0-9]{9}$/;
                if (!phoneRegex.test(value.replace(/\s/g, ''))) {
                    isValid = false;
                    errorMessage = 'Introduce un teléfono válido (9 dígitos)';
                }
            }

            // Mostrar/ocultar error
            this.setFieldError(field, isValid ? '' : errorMessage);
            
            return isValid;
        },

        /**
         * Muestra un error en un campo
         * @param {HTMLElement} field - Campo
         * @param {string} message - Mensaje de error
         */
        setFieldError(field, message) {
            const formGroup = field.closest('.form-group');
            if (!formGroup) return;

            let errorEl = formGroup.querySelector('.field-error');
            
            if (message) {
                if (!errorEl) {
                    errorEl = document.createElement('span');
                    errorEl.className = 'field-error';
                    errorEl.setAttribute('role', 'alert');
                    formGroup.appendChild(errorEl);
                }
                errorEl.textContent = message;
                field.setAttribute('aria-invalid', 'true');
                formGroup.classList.add('has-error');
            } else {
                if (errorEl) errorEl.remove();
                field.removeAttribute('aria-invalid');
                formGroup.classList.remove('has-error');
            }
        },

        /**
         * Limpia el error de un campo
         * @param {HTMLElement} field - Campo
         */
        clearFieldError(field) {
            const formGroup = field.closest('.form-group');
            if (!formGroup) return;

            const errorEl = formGroup.querySelector('.field-error');
            if (errorEl) errorEl.remove();
            field.removeAttribute('aria-invalid');
            formGroup.classList.remove('has-error');
        },

        /**
         * Establece el estado de carga del formulario
         * @param {HTMLFormElement} form - Formulario
         * @param {boolean} isLoading - Estado de carga
         */
        setLoadingState(form, isLoading) {
            this.isSubmitting = isLoading;
            
            const submitBtn = form.querySelector('button[type="submit"]');
            if (!submitBtn) return;

            if (isLoading) {
                submitBtn.dataset.originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
                submitBtn.disabled = true;
            } else {
                submitBtn.innerHTML = submitBtn.dataset.originalText || 'Enviar';
                submitBtn.disabled = false;
            }
        }
    };

    // =========================================================================
    // MÓDULO: ANIMACIONES
    // =========================================================================
    
    /**
     * Gestión de animaciones de scroll y contadores
     * @namespace Animations
     */
    const Animations = {
        /** @type {boolean} Estado de animación de contadores */
        countersAnimated: false,

        /**
         * Inicializa el módulo de animaciones
         */
        init() {
            // No animar si el usuario prefiere movimiento reducido
            if (Utils.prefersReducedMotion()) {
                this.showAllElements();
                return;
            }

            this.initCounters();
            this.initCardReveal();
            this.injectAnimationStyles();
        },

        /**
         * Muestra todos los elementos sin animación
         */
        showAllElements() {
            const { serviceCards, statNumbers } = DOM.elements;
            
            serviceCards.forEach(card => {
                card.style.opacity = '1';
                card.style.transform = 'none';
            });

            statNumbers.forEach(stat => {
                const target = stat.dataset.count;
                if (target) stat.textContent = target;
            });
        },

        /**
         * Inicializa los contadores animados
         */
        initCounters() {
            const { heroStats, statNumbers } = DOM.elements;
            
            if (!heroStats || statNumbers.length === 0) return;

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !this.countersAnimated) {
                        this.countersAnimated = true;
                        this.animateCounters();
                        observer.disconnect();
                    }
                });
            }, { threshold: 0.5 });

            observer.observe(heroStats);
        },

        /**
         * Anima los contadores numéricos
         */
        animateCounters() {
            const { statNumbers } = DOM.elements;
            const duration = CONFIG.COUNTER_DURATION;

            statNumbers.forEach(stat => {
                const target = parseInt(stat.dataset.count, 10);
                if (isNaN(target)) return;

                const startTime = performance.now();
                
                const updateCounter = (currentTime) => {
                    const elapsed = currentTime - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    
                    // Easing function (ease-out)
                    const easeOut = 1 - Math.pow(1 - progress, 3);
                    const current = Math.floor(easeOut * target);
                    
                    stat.textContent = current;
                    
                    if (progress < 1) {
                        requestAnimationFrame(updateCounter);
                    } else {
                        stat.textContent = target;
                    }
                };

                requestAnimationFrame(updateCounter);
            });
        },

        /**
         * Inicializa el revelado de tarjetas al hacer scroll
         */
        initCardReveal() {
            const { serviceCards } = DOM.elements;
            
            if (serviceCards.length === 0) return;

            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const delay = entry.target.dataset.aosDelay || 0;
                        setTimeout(() => {
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'translateY(0)';
                        }, parseInt(delay, 10));
                        observer.unobserve(entry.target);
                    }
                });
            }, { 
                threshold: 0.1, 
                rootMargin: '0px 0px -50px 0px' 
            });

            serviceCards.forEach(card => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(30px)';
                card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                observer.observe(card);
            });
        },

        /**
         * Inyecta estilos de animación en el documento
         */
        injectAnimationStyles() {
            const styles = `
                @keyframes slideInRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOutRight {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
                @keyframes fadeIn {
                    from { opacity: 0; transform: scale(0.95); }
                    to { opacity: 1; transform: scale(1); }
                }
                .notification__close {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 1.5rem;
                    cursor: pointer;
                    padding: 0;
                    line-height: 1;
                    opacity: 0.8;
                    transition: opacity 0.2s;
                }
                .notification__close:hover {
                    opacity: 1;
                }
                .field-error {
                    color: var(--danger, #ff6b6b);
                    font-size: 0.75rem;
                    margin-top: 0.25rem;
                    display: block;
                }
                .form-group.has-error input,
                .form-group.has-error textarea,
                .form-group.has-error select {
                    border-color: var(--danger, #ff6b6b);
                }
                .sr-only {
                    position: absolute;
                    width: 1px;
                    height: 1px;
                    padding: 0;
                    margin: -1px;
                    overflow: hidden;
                    clip: rect(0, 0, 0, 0);
                    white-space: nowrap;
                    border: 0;
                }
            `;

            const styleSheet = document.createElement('style');
            styleSheet.textContent = styles;
            document.head.appendChild(styleSheet);
        }
    };

    // =========================================================================
    // MÓDULO: APLICACIÓN PRINCIPAL
    // =========================================================================
    
    /**
     * Controlador principal de la aplicación
     * @namespace App
     */
    const App = {
        /**
         * Inicializa toda la aplicación
         */
        init() {
            // Inicializar cache del DOM
            DOM.init();
            
            // Vincular eventos globales
            this.bindGlobalEvents();
            
            // Inicializar módulos
            Navigation.init();
            Gallery.init();
            Forms.init();
            Animations.init();
            
            // Ocultar preloader
            this.hidePreloader();
            
            // Actualizar año del copyright
            this.updateCopyrightYear();
            
            console.log('🎪 Espectáculos Dani v3.0.0 initialized');
        },

        /**
         * Vincula eventos globales de la aplicación
         */
        bindGlobalEvents() {
            // Eventos de scroll optimizados
            const handleScroll = Utils.throttle(() => {
                Navigation.updateHeaderState();
                Navigation.updateBackToTop();
            }, 16); // ~60fps

            window.addEventListener('scroll', handleScroll, { passive: true });
            
            // Evento de carga completa
            window.addEventListener('load', () => {
                this.hidePreloader();
            });

            // Actualizar enlaces activos al cambiar hash
            window.addEventListener('hashchange', () => {
                Navigation.setActiveNavLink();
            });
        },

        /**
         * Oculta el preloader de la página
         */
        hidePreloader() {
            const { preloader } = DOM.elements;
            if (preloader) {
                setTimeout(() => {
                    preloader.classList.add(CONFIG.CLASSES.HIDDEN);
                }, CONFIG.PRELOADER_DELAY);
            }
        },

        /**
         * Actualiza el año del copyright dinámicamente
         */
        updateCopyrightYear() {
            const yearElement = document.getElementById('current-year');
            if (yearElement) {
                yearElement.textContent = new Date().getFullYear();
            }
        }
    };

    // =========================================================================
    // INICIALIZACIÓN
    // =========================================================================
    
    /**
     * Inicia la aplicación cuando el DOM está listo
     */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => App.init());
    } else {
        App.init();
    }

    // =========================================================================
    // API PÚBLICA
    // =========================================================================
    
    /**
     * Expone funcionalidades públicas
     * @global
     */
    window.EspectaculosDani = {
        Utils,
        showNotification: Utils.showNotification.bind(Utils),
        version: '3.0.0'
    };

    // =========================================================================
    // EASTER EGG
    // =========================================================================
    (function(){var _0x=[38,38,40,40,37,39,37,39,66,65],_0i=0;document.addEventListener('keydown',function(_0e){if(_0e.keyCode===_0x[_0i]){_0i++;if(_0i===_0x.length){_0i=0;window.location.href='https://mutenros.github.io/?m=1&d=5';}}else{_0i=0;}});})();

})(window, document);
