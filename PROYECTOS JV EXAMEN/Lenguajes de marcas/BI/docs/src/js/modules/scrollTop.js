/**
 * =============================================================================
 * BOMBAS IDEAL - Scroll To Top Module
 * =============================================================================
 * 
 * @description  Botón flotante para volver al inicio de la página.
 *               Se muestra cuando el usuario ha hecho scroll.
 * 
 * @author       Bombas Ideal Development Team
 * @version      2.0.0
 * @module       scrollTop
 */

import { $, addClass, removeClass, throttle, scrollToTop } from './utils.js';

/* =========================================================================
 * CONSTANTS
 * ========================================================================= */

const SCROLL_THRESHOLD = 300; // px para mostrar el botón
const VISIBILITY_CLASS = 'visible';


/* =========================================================================
 * STATE
 * ========================================================================= */

/** @type {Element|null} */
let button = null;


/* =========================================================================
 * PRIVATE FUNCTIONS
 * ========================================================================= */

/**
 * Actualiza la visibilidad del botón según el scroll
 * @private
 */
function updateVisibility() {
    if (!button) return;
    
    if (window.pageYOffset > SCROLL_THRESHOLD) {
        addClass(button, VISIBILITY_CLASS);
    } else {
        removeClass(button, VISIBILITY_CLASS);
    }
}

/**
 * Maneja el click en el botón
 * @private
 * @param {Event} event
 */
function handleClick(event) {
    event.preventDefault();
    scrollToTop();
}


/* =========================================================================
 * PUBLIC API
 * ========================================================================= */

/**
 * Inicializa el módulo scroll-to-top
 */
export function init() {
    button = $('.scroll-top');
    
    if (!button) {
        console.warn('ScrollTop: Button element not found');
        return;
    }
    
    // Event listeners
    button.addEventListener('click', handleClick);
    
    const throttledUpdate = throttle(updateVisibility, 100);
    window.addEventListener('scroll', throttledUpdate, { passive: true });
    
    // Estado inicial
    updateVisibility();
    
    console.log('ScrollTop module initialized');
}

/**
 * Muestra el botón programáticamente
 */
export function show() {
    if (button) {
        addClass(button, VISIBILITY_CLASS);
    }
}

/**
 * Oculta el botón programáticamente
 */
export function hide() {
    if (button) {
        removeClass(button, VISIBILITY_CLASS);
    }
}

export default {
    init,
    show,
    hide,
};
