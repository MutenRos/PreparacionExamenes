/**
 * =============================================================================
 * BOMBAS IDEAL - Utilities Module
 * =============================================================================
 * 
 * @description  Funciones de utilidad reutilizables en toda la aplicación.
 *               Incluye helpers para DOM, eventos, strings, y más.
 * 
 * @author       Bombas Ideal Development Team
 * @version      2.0.0
 * @module       utils
 */

/* =========================================================================
 * DOM UTILITIES
 * ========================================================================= */

/**
 * Selecciona un elemento del DOM (shorthand para querySelector)
 * @param {string} selector - Selector CSS
 * @param {Element} [context=document] - Contexto de búsqueda
 * @returns {Element|null}
 */
export function $(selector, context = document) {
    return context.querySelector(selector);
}

/**
 * Selecciona múltiples elementos del DOM (shorthand para querySelectorAll)
 * @param {string} selector - Selector CSS
 * @param {Element} [context=document] - Contexto de búsqueda
 * @returns {Element[]} - Array de elementos (no NodeList)
 */
export function $$(selector, context = document) {
    return [...context.querySelectorAll(selector)];
}

/**
 * Verifica si un elemento existe en el DOM
 * @param {string} selector - Selector CSS
 * @returns {boolean}
 */
export function exists(selector) {
    return $(selector) !== null;
}

/**
 * Añade una clase a un elemento de forma segura
 * @param {Element|string} element - Elemento o selector
 * @param {string} className - Clase a añadir
 */
export function addClass(element, className) {
    const el = typeof element === 'string' ? $(element) : element;
    if (el) el.classList.add(className);
}

/**
 * Elimina una clase de un elemento de forma segura
 * @param {Element|string} element - Elemento o selector
 * @param {string} className - Clase a eliminar
 */
export function removeClass(element, className) {
    const el = typeof element === 'string' ? $(element) : element;
    if (el) el.classList.remove(className);
}

/**
 * Alterna una clase en un elemento de forma segura
 * @param {Element|string} element - Elemento o selector
 * @param {string} className - Clase a alternar
 * @returns {boolean|undefined} - Nuevo estado de la clase
 */
export function toggleClass(element, className) {
    const el = typeof element === 'string' ? $(element) : element;
    if (el) return el.classList.toggle(className);
}

/**
 * Verifica si un elemento tiene una clase
 * @param {Element|string} element - Elemento o selector
 * @param {string} className - Clase a verificar
 * @returns {boolean}
 */
export function hasClass(element, className) {
    const el = typeof element === 'string' ? $(element) : element;
    return el ? el.classList.contains(className) : false;
}


/* =========================================================================
 * EVENT UTILITIES
 * ========================================================================= */

/**
 * Añade event listener con delegación de eventos
 * @param {Element|string} parent - Elemento padre o selector
 * @param {string} eventType - Tipo de evento
 * @param {string} childSelector - Selector del hijo
 * @param {Function} callback - Función callback
 */
export function delegate(parent, eventType, childSelector, callback) {
    const el = typeof parent === 'string' ? $(parent) : parent;
    if (!el) return;
    
    el.addEventListener(eventType, (event) => {
        const target = event.target.closest(childSelector);
        if (target && el.contains(target)) {
            callback.call(target, event, target);
        }
    });
}

/**
 * Ejecuta callback cuando el DOM está listo
 * @param {Function} callback - Función a ejecutar
 */
export function onReady(callback) {
    if (document.readyState !== 'loading') {
        callback();
    } else {
        document.addEventListener('DOMContentLoaded', callback);
    }
}

/**
 * Crea una función debounced (retrasa ejecución)
 * @param {Function} func - Función a ejecutar
 * @param {number} wait - Tiempo de espera en ms
 * @returns {Function}
 */
export function debounce(func, wait) {
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

/**
 * Crea una función throttled (limita frecuencia de ejecución)
 * @param {Function} func - Función a ejecutar
 * @param {number} limit - Tiempo mínimo entre ejecuciones en ms
 * @returns {Function}
 */
export function throttle(func, limit) {
    let inThrottle;
    return function executedFunction(...args) {
        if (!inThrottle) {
            func(...args);
            inThrottle = true;
            setTimeout(() => (inThrottle = false), limit);
        }
    };
}


/* =========================================================================
 * SCROLL UTILITIES
 * ========================================================================= */

/**
 * Scroll suave a un elemento
 * @param {Element|string} target - Elemento o selector destino
 * @param {Object} [options] - Opciones de scroll
 * @param {number} [options.offset=0] - Offset desde el top
 * @param {string} [options.behavior='smooth'] - Comportamiento del scroll
 */
export function scrollTo(target, options = {}) {
    const { offset = 0, behavior = 'smooth' } = options;
    const el = typeof target === 'string' ? $(target) : target;
    
    if (!el) return;
    
    const top = el.getBoundingClientRect().top + window.pageYOffset - offset;
    
    window.scrollTo({
        top,
        behavior,
    });
}

/**
 * Scroll suave al top de la página
 * @param {string} [behavior='smooth'] - Comportamiento del scroll
 */
export function scrollToTop(behavior = 'smooth') {
    window.scrollTo({ top: 0, behavior });
}

/**
 * Obtiene la posición actual del scroll
 * @returns {Object} - { x, y }
 */
export function getScrollPosition() {
    return {
        x: window.pageXOffset || document.documentElement.scrollLeft,
        y: window.pageYOffset || document.documentElement.scrollTop,
    };
}

/**
 * Verifica si un elemento está en el viewport
 * @param {Element} element - Elemento a verificar
 * @param {number} [threshold=0] - Margen adicional
 * @returns {boolean}
 */
export function isInViewport(element, threshold = 0) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) + threshold &&
        rect.bottom >= -threshold &&
        rect.left <= (window.innerWidth || document.documentElement.clientWidth) + threshold &&
        rect.right >= -threshold
    );
}


/* =========================================================================
 * STRING UTILITIES
 * ========================================================================= */

/**
 * Capitaliza la primera letra de un string
 * @param {string} str - String a capitalizar
 * @returns {string}
 */
export function capitalize(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

/**
 * Genera un ID único
 * @param {string} [prefix='id'] - Prefijo del ID
 * @returns {string}
 */
export function uniqueId(prefix = 'id') {
    return `${prefix}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Formatea un número con separador de miles
 * @param {number} num - Número a formatear
 * @param {string} [locale='es-ES'] - Locale para formateo
 * @returns {string}
 */
export function formatNumber(num, locale = 'es-ES') {
    return new Intl.NumberFormat(locale).format(num);
}


/* =========================================================================
 * STORAGE UTILITIES
 * ========================================================================= */

/**
 * Guarda datos en localStorage con manejo de errores
 * @param {string} key - Clave
 * @param {*} value - Valor (se serializa automáticamente)
 * @returns {boolean} - Éxito de la operación
 */
export function setStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (e) {
        console.warn('Error saving to localStorage:', e);
        return false;
    }
}

/**
 * Obtiene datos de localStorage con manejo de errores
 * @param {string} key - Clave
 * @param {*} [defaultValue=null] - Valor por defecto si no existe
 * @returns {*}
 */
export function getStorage(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (e) {
        console.warn('Error reading from localStorage:', e);
        return defaultValue;
    }
}

/**
 * Elimina datos de localStorage
 * @param {string} key - Clave a eliminar
 */
export function removeStorage(key) {
    try {
        localStorage.removeItem(key);
    } catch (e) {
        console.warn('Error removing from localStorage:', e);
    }
}


/* =========================================================================
 * MISC UTILITIES
 * ========================================================================= */

/**
 * Espera un tiempo determinado (para usar con async/await)
 * @param {number} ms - Milisegundos a esperar
 * @returns {Promise}
 */
export function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Detecta si el dispositivo tiene capacidades táctiles
 * @returns {boolean}
 */
export function isTouchDevice() {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

/**
 * Copia texto al portapapeles
 * @param {string} text - Texto a copiar
 * @returns {Promise<boolean>} - Éxito de la operación
 */
export async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (e) {
        console.warn('Error copying to clipboard:', e);
        return false;
    }
}

export default {
    $,
    $$,
    exists,
    addClass,
    removeClass,
    toggleClass,
    hasClass,
    delegate,
    onReady,
    debounce,
    throttle,
    scrollTo,
    scrollToTop,
    getScrollPosition,
    isInViewport,
    capitalize,
    uniqueId,
    formatNumber,
    setStorage,
    getStorage,
    removeStorage,
    sleep,
    isTouchDevice,
    copyToClipboard,
};
