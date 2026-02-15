/**
 * =============================================================================
 * BOMBAS IDEAL - Navigation Module
 * =============================================================================
 * 
 * @description  Gestiona toda la funcionalidad de navegación:
 *               - Navbar sticky con cambio en scroll
 *               - Menú móvil (hamburger)
 *               - Dropdowns
 *               - Smooth scroll para anchor links
 *               - Top bar hide on scroll
 * 
 * @author       Bombas Ideal Development Team
 * @version      2.0.0
 * @module       navigation
 */

import { $, $$, addClass, removeClass, hasClass, toggleClass, throttle } from './utils.js';
import { CONFIG, isMobile } from '../config.js';

/* =========================================================================
 * STATE
 * ========================================================================= */

/** @type {Object} Estado interno del módulo */
const state = {
    isMenuOpen: false,
    lastScrollY: 0,
    isScrollingDown: false,
};


/* =========================================================================
 * DOM ELEMENTS
 * ========================================================================= */

/** @type {Object} Referencias a elementos del DOM */
let elements = {
    topBar: null,
    navbar: null,
    hamburger: null,
    navMenu: null,
    navLinks: null,
    dropdowns: null,
};


/* =========================================================================
 * PRIVATE FUNCTIONS
 * ========================================================================= */

/**
 * Cachea las referencias a elementos del DOM
 * @private
 */
function cacheElements() {
    elements = {
        topBar: $('.top-bar'),
        navbar: $('.navbar'),
        hamburger: $('.hamburger'),
        navMenu: $('.nav-menu'),
        navLinks: $$('.nav-link'),
        dropdowns: $$('.has-dropdown'),
    };
}

/**
 * Maneja el scroll de la página
 * Actualiza el estado de la navbar y el top bar
 * @private
 */
function handleScroll() {
    const currentScrollY = window.pageYOffset;
    const { scrollThreshold, hideTopBarOnScroll } = CONFIG.navigation;
    
    // Determinar dirección del scroll
    state.isScrollingDown = currentScrollY > state.lastScrollY;
    state.lastScrollY = currentScrollY;
    
    // Navbar scrolled state
    if (elements.navbar) {
        if (currentScrollY > scrollThreshold) {
            addClass(elements.navbar, 'scrolled');
        } else {
            removeClass(elements.navbar, 'scrolled');
        }
    }
    
    // Ocultar top bar en scroll (solo si está configurado)
    if (elements.topBar && hideTopBarOnScroll) {
        if (currentScrollY > scrollThreshold && state.isScrollingDown) {
            addClass(elements.topBar, 'hidden');
        } else {
            removeClass(elements.topBar, 'hidden');
        }
    }
}

/**
 * Abre el menú móvil
 * @private
 */
function openMenu() {
    state.isMenuOpen = true;
    addClass(elements.hamburger, 'active');
    addClass(elements.navMenu, 'active');
    document.body.style.overflow = 'hidden';
}

/**
 * Cierra el menú móvil
 * @private
 */
function closeMenu() {
    state.isMenuOpen = false;
    removeClass(elements.hamburger, 'active');
    removeClass(elements.navMenu, 'active');
    document.body.style.overflow = '';
    
    // Cerrar también todos los dropdowns
    elements.dropdowns.forEach(dropdown => {
        removeClass(dropdown, 'open');
    });
}

/**
 * Alterna el menú móvil
 * @private
 */
function toggleMenu() {
    if (state.isMenuOpen) {
        closeMenu();
    } else {
        openMenu();
    }
}

/**
 * Maneja el click en un dropdown (móvil)
 * @private
 * @param {Event} event - Evento click
 */
function handleDropdownClick(event) {
    // Solo en móvil
    if (!isMobile()) return;
    
    const dropdown = event.currentTarget;
    const link = dropdown.querySelector('.nav-link');
    
    // Prevenir navegación si tiene submenú
    if (dropdown.querySelector('.dropdown-menu')) {
        event.preventDefault();
        toggleClass(dropdown, 'open');
    }
}

/**
 * Maneja smooth scroll para anchor links
 * @private
 * @param {Event} event - Evento click
 */
function handleAnchorClick(event) {
    const link = event.currentTarget;
    const href = link.getAttribute('href');
    
    // Solo procesar anchor links internos
    if (!href || !href.startsWith('#') || href === '#') return;
    
    const target = $(href);
    if (!target) return;
    
    event.preventDefault();
    
    // Calcular offset (altura de la navbar)
    const navbarHeight = elements.navbar ? elements.navbar.offsetHeight : 0;
    const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
    const offsetPosition = targetPosition - navbarHeight - 20;
    
    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth',
    });
    
    // Cerrar menú móvil si está abierto
    if (state.isMenuOpen) {
        closeMenu();
    }
}

/**
 * Actualiza el link activo basado en la sección visible
 * @private
 */
function updateActiveLink() {
    const sections = $$('section[id]');
    const navbarHeight = elements.navbar ? elements.navbar.offsetHeight : 0;
    
    let currentSection = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop - navbarHeight - 100;
        const sectionHeight = section.offsetHeight;
        
        if (window.pageYOffset >= sectionTop && 
            window.pageYOffset < sectionTop + sectionHeight) {
            currentSection = section.getAttribute('id');
        }
    });
    
    elements.navLinks.forEach(link => {
        removeClass(link, 'active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            addClass(link, 'active');
        }
    });
}

/**
 * Cierra el menú al hacer click fuera
 * @private
 * @param {Event} event - Evento click
 */
function handleOutsideClick(event) {
    if (!state.isMenuOpen) return;
    
    const isClickInsideMenu = elements.navMenu.contains(event.target);
    const isClickOnHamburger = elements.hamburger.contains(event.target);
    
    if (!isClickInsideMenu && !isClickOnHamburger) {
        closeMenu();
    }
}

/**
 * Cierra el menú con tecla Escape
 * @private
 * @param {KeyboardEvent} event - Evento teclado
 */
function handleEscapeKey(event) {
    if (event.key === 'Escape' && state.isMenuOpen) {
        closeMenu();
    }
}

/**
 * Maneja el resize de la ventana
 * @private
 */
function handleResize() {
    // Cerrar menú móvil si cambiamos a desktop
    if (!isMobile() && state.isMenuOpen) {
        closeMenu();
    }
}


/* =========================================================================
 * PUBLIC API
 * ========================================================================= */

/**
 * Inicializa el módulo de navegación
 * Configura todos los event listeners necesarios
 */
export function init() {
    cacheElements();
    
    // Verificar que existan los elementos necesarios
    if (!elements.navbar) {
        console.warn('Navigation: Navbar element not found');
        return;
    }
    
    // Event listeners
    
    // Scroll (throttled para performance)
    const throttledScroll = throttle(handleScroll, 100);
    window.addEventListener('scroll', throttledScroll, { passive: true });
    
    // También actualizar link activo en scroll
    const throttledActiveLink = throttle(updateActiveLink, 200);
    window.addEventListener('scroll', throttledActiveLink, { passive: true });
    
    // Hamburger menu
    if (elements.hamburger) {
        elements.hamburger.addEventListener('click', toggleMenu);
    }
    
    // Dropdowns en móvil
    elements.dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', handleDropdownClick);
    });
    
    // Anchor links (smooth scroll)
    elements.navLinks.forEach(link => {
        link.addEventListener('click', handleAnchorClick);
    });
    
    // Cerrar al click fuera
    document.addEventListener('click', handleOutsideClick);
    
    // Cerrar con Escape
    document.addEventListener('keydown', handleEscapeKey);
    
    // Resize
    window.addEventListener('resize', throttle(handleResize, 200));
    
    // Estado inicial
    handleScroll();
    updateActiveLink();
    
    console.log('Navigation module initialized');
}

/**
 * Cierra el menú móvil programáticamente
 */
export function close() {
    closeMenu();
}

/**
 * Abre el menú móvil programáticamente
 */
export function open() {
    if (isMobile()) {
        openMenu();
    }
}

/**
 * Obtiene el estado actual del menú
 * @returns {boolean}
 */
export function isOpen() {
    return state.isMenuOpen;
}

export default {
    init,
    open,
    close,
    isOpen,
};
