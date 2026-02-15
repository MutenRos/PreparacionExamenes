/**
 * =============================================================================
 * BOMBAS IDEAL - Animations Module
 * =============================================================================
 * 
 * @description  Sistema de animaciones basado en Intersection Observer.
 *               Detecta cuando los elementos entran en el viewport y
 *               les aplica animaciones de entrada.
 * 
 * @author       Bombas Ideal Development Team
 * @version      2.0.0
 * @module       animations
 */

import { $, $$, addClass, removeClass } from './utils.js';
import { CONFIG, prefersReducedMotion, getAnimationDuration } from '../config.js';

/* =========================================================================
 * STATE
 * ========================================================================= */

/** @type {IntersectionObserver|null} */
let observer = null;

/** @type {boolean} */
let isInitialized = false;


/* =========================================================================
 * ANIMATION CLASSES
 * ========================================================================= */

/**
 * Clases de animación disponibles
 * Usar data-animate="fadeIn" en el HTML
 */
const ANIMATIONS = {
    // Fade
    fadeIn: 'animate-fade-in',
    fadeUp: 'animate-fade-up',
    fadeDown: 'animate-fade-down',
    fadeLeft: 'animate-fade-left',
    fadeRight: 'animate-fade-right',
    
    // Scale
    scaleIn: 'animate-scale-in',
    scaleUp: 'animate-scale-up',
    
    // Slide
    slideUp: 'animate-slide-up',
    slideDown: 'animate-slide-down',
    slideLeft: 'animate-slide-left',
    slideRight: 'animate-slide-right',
    
    // Otros
    bounce: 'animate-bounce-in',
    flip: 'animate-flip',
};


/* =========================================================================
 * PRIVATE FUNCTIONS
 * ========================================================================= */

/**
 * Callback del Intersection Observer
 * @private
 * @param {IntersectionObserverEntry[]} entries
 */
function handleIntersection(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const element = entry.target;
            const animationType = element.dataset.animate;
            const animationClass = ANIMATIONS[animationType] || ANIMATIONS.fadeIn;
            const delay = element.dataset.animateDelay || 0;
            
            // Aplicar delay si existe
            if (delay) {
                element.style.animationDelay = `${delay}ms`;
            }
            
            // Aplicar animación
            addClass(element, 'is-visible');
            addClass(element, animationClass);
            
            // Dejar de observar el elemento
            observer.unobserve(element);
        }
    });
}

/**
 * Crea el Intersection Observer
 * @private
 */
function createObserver() {
    const options = {
        root: null, // viewport
        rootMargin: '0px 0px -50px 0px',
        threshold: CONFIG.animations.observerThreshold,
    };
    
    observer = new IntersectionObserver(handleIntersection, options);
}

/**
 * Añade los estilos CSS necesarios para las animaciones
 * @private
 */
function injectStyles() {
    // Verificar si ya existen
    if ($('#bi-animation-styles')) return;
    
    const duration = getAnimationDuration();
    const easing = CONFIG.animations.easing;
    
    const styles = document.createElement('style');
    styles.id = 'bi-animation-styles';
    styles.textContent = `
        /* Estado inicial de elementos animables */
        [data-animate] {
            opacity: 0;
        }
        
        [data-animate].is-visible {
            opacity: 1;
        }
        
        /* Fade animations */
        .animate-fade-in {
            animation: fadeIn ${duration}ms ${easing} forwards;
        }
        
        .animate-fade-up {
            animation: fadeUp ${duration}ms ${easing} forwards;
        }
        
        .animate-fade-down {
            animation: fadeDown ${duration}ms ${easing} forwards;
        }
        
        .animate-fade-left {
            animation: fadeLeft ${duration}ms ${easing} forwards;
        }
        
        .animate-fade-right {
            animation: fadeRight ${duration}ms ${easing} forwards;
        }
        
        /* Scale animations */
        .animate-scale-in {
            animation: scaleIn ${duration}ms ${easing} forwards;
        }
        
        .animate-scale-up {
            animation: scaleUp ${duration}ms ${easing} forwards;
        }
        
        /* Slide animations */
        .animate-slide-up {
            animation: slideUp ${duration}ms ${easing} forwards;
        }
        
        .animate-slide-down {
            animation: slideDown ${duration}ms ${easing} forwards;
        }
        
        /* Keyframes */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeLeft {
            from {
                opacity: 0;
                transform: translateX(30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes fadeRight {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes scaleIn {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        @keyframes scaleUp {
            from {
                opacity: 0;
                transform: scale(0.5);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(100%);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-100%);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes bounceIn {
            0% {
                opacity: 0;
                transform: scale(0.3);
            }
            50% {
                transform: scale(1.05);
            }
            70% {
                transform: scale(0.9);
            }
            100% {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        /* Reduced motion */
        @media (prefers-reduced-motion: reduce) {
            [data-animate] {
                opacity: 1 !important;
                transform: none !important;
                animation: none !important;
            }
        }
    `;
    
    document.head.appendChild(styles);
}


/* =========================================================================
 * PUBLIC API
 * ========================================================================= */

/**
 * Inicializa el módulo de animaciones
 */
export function init() {
    // No inicializar si prefiere reduced motion
    if (prefersReducedMotion()) {
        // Mostrar todos los elementos inmediatamente
        $$('[data-animate]').forEach(el => {
            el.style.opacity = '1';
        });
        console.log('Animations: Disabled (reduced motion preference)');
        return;
    }
    
    // No inicializar si las animaciones están deshabilitadas
    if (!CONFIG.animations.enabled) {
        $$('[data-animate]').forEach(el => {
            el.style.opacity = '1';
        });
        console.log('Animations: Disabled (config)');
        return;
    }
    
    // Inyectar estilos
    injectStyles();
    
    // Crear observer
    createObserver();
    
    // Observar todos los elementos con data-animate
    const animatables = $$('[data-animate]');
    animatables.forEach(el => observer.observe(el));
    
    isInitialized = true;
    console.log(`Animations module initialized (${animatables.length} elements)`);
}

/**
 * Añade un nuevo elemento al observer
 * @param {Element} element - Elemento a observar
 */
export function observe(element) {
    if (!isInitialized || !observer) return;
    observer.observe(element);
}

/**
 * Deja de observar un elemento
 * @param {Element} element - Elemento a dejar de observar
 */
export function unobserve(element) {
    if (!observer) return;
    observer.unobserve(element);
}

/**
 * Fuerza la animación de un elemento inmediatamente
 * @param {Element} element - Elemento a animar
 */
export function animate(element) {
    if (prefersReducedMotion()) return;
    
    const animationType = element.dataset.animate || 'fadeIn';
    const animationClass = ANIMATIONS[animationType] || ANIMATIONS.fadeIn;
    
    addClass(element, 'is-visible');
    addClass(element, animationClass);
}

/**
 * Resetea un elemento para poder re-animarlo
 * @param {Element} element - Elemento a resetear
 */
export function reset(element) {
    removeClass(element, 'is-visible');
    Object.values(ANIMATIONS).forEach(cls => {
        removeClass(element, cls);
    });
}

/**
 * Destruye el módulo y limpia recursos
 */
export function destroy() {
    if (observer) {
        observer.disconnect();
        observer = null;
    }
    isInitialized = false;
}

export default {
    init,
    observe,
    unobserve,
    animate,
    reset,
    destroy,
};
