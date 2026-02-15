/**
 * =============================================================================
 * BOMBAS IDEAL - Modals Module
 * =============================================================================
 * 
 * @description  Sistema de ventanas modales. Soporta apertura/cierre
 *               programático, click en overlay para cerrar, y tecla Escape.
 * 
 * @author       Bombas Ideal Development Team
 * @version      2.0.0
 * @module       modals
 */

import { $, $$, addClass, removeClass, hasClass, delegate } from './utils.js';

/* =========================================================================
 * CONSTANTS
 * ========================================================================= */

const ACTIVE_CLASS = 'active';
const BODY_CLASS = 'modal-open';


/* =========================================================================
 * STATE
 * ========================================================================= */

/** @type {Element|null} Modal actualmente abierto */
let currentModal = null;

/** @type {Element|null} Elemento que tenía foco antes de abrir */
let previousFocus = null;


/* =========================================================================
 * PRIVATE FUNCTIONS
 * ========================================================================= */

/**
 * Maneja el click en el overlay
 * @private
 * @param {Event} event
 */
function handleOverlayClick(event) {
    if (event.target.classList.contains('modal-overlay')) {
        close();
    }
}

/**
 * Maneja la tecla Escape
 * @private
 * @param {KeyboardEvent} event
 */
function handleEscape(event) {
    if (event.key === 'Escape' && currentModal) {
        close();
    }
}

/**
 * Maneja el click en botones de cerrar
 * @private
 * @param {Event} event
 */
function handleCloseClick(event) {
    const closeBtn = event.target.closest('[data-modal-close]');
    if (closeBtn) {
        close();
    }
}

/**
 * Maneja el click en triggers de apertura
 * @private
 * @param {Event} event
 */
function handleTriggerClick(event) {
    const trigger = event.target.closest('[data-modal-open]');
    if (trigger) {
        event.preventDefault();
        const modalId = trigger.dataset.modalOpen;
        open(modalId);
    }
}

/**
 * Atrapa el foco dentro del modal
 * @private
 * @param {KeyboardEvent} event
 */
function trapFocus(event) {
    if (!currentModal || event.key !== 'Tab') return;
    
    const focusables = currentModal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstFocusable = focusables[0];
    const lastFocusable = focusables[focusables.length - 1];
    
    if (event.shiftKey) {
        // Shift + Tab
        if (document.activeElement === firstFocusable) {
            event.preventDefault();
            lastFocusable.focus();
        }
    } else {
        // Tab
        if (document.activeElement === lastFocusable) {
            event.preventDefault();
            firstFocusable.focus();
        }
    }
}


/* =========================================================================
 * PUBLIC API
 * ========================================================================= */

/**
 * Inicializa el módulo de modales
 */
export function init() {
    // Event delegation para triggers y close buttons
    document.addEventListener('click', handleTriggerClick);
    document.addEventListener('click', handleCloseClick);
    document.addEventListener('click', handleOverlayClick);
    
    // Escape para cerrar
    document.addEventListener('keydown', handleEscape);
    
    // Trap focus
    document.addEventListener('keydown', trapFocus);
    
    console.log('Modals module initialized');
}

/**
 * Abre un modal
 * @param {string|Element} modal - ID del modal o elemento
 */
export function open(modal) {
    const modalEl = typeof modal === 'string' ? $(`#${modal}`) : modal;
    
    if (!modalEl) {
        console.warn(`Modal not found: ${modal}`);
        return;
    }
    
    // Guardar foco actual
    previousFocus = document.activeElement;
    
    // Cerrar modal anterior si existe
    if (currentModal) {
        close();
    }
    
    // Abrir nuevo modal
    currentModal = modalEl;
    addClass(modalEl, ACTIVE_CLASS);
    addClass(document.body, BODY_CLASS);
    
    // Mover foco al modal
    const firstFocusable = modalEl.querySelector(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    if (firstFocusable) {
        firstFocusable.focus();
    }
    
    // Disparar evento
    modalEl.dispatchEvent(new CustomEvent('modal:open'));
}

/**
 * Cierra el modal actual
 */
export function close() {
    if (!currentModal) return;
    
    const modal = currentModal;
    
    removeClass(modal, ACTIVE_CLASS);
    removeClass(document.body, BODY_CLASS);
    
    // Restaurar foco
    if (previousFocus) {
        previousFocus.focus();
        previousFocus = null;
    }
    
    // Disparar evento
    modal.dispatchEvent(new CustomEvent('modal:close'));
    
    currentModal = null;
}

/**
 * Verifica si hay un modal abierto
 * @returns {boolean}
 */
export function isOpen() {
    return currentModal !== null;
}

/**
 * Obtiene el modal actualmente abierto
 * @returns {Element|null}
 */
export function getCurrent() {
    return currentModal;
}

export default {
    init,
    open,
    close,
    isOpen,
    getCurrent,
};
