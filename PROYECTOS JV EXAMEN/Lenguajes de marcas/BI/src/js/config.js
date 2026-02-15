/**
 * =============================================================================
 * BOMBAS IDEAL - Configuration Module
 * =============================================================================
 * 
 * @description  Configuración centralizada de la aplicación. Contiene
 *               constantes, valores por defecto y opciones configurables.
 * 
 * @author       Bombas Ideal Development Team
 * @version      2.0.0
 * @module       config
 */

/**
 * Configuración global de la aplicación
 * @constant {Object}
 */
export const CONFIG = {
    /**
     * Información de la empresa
     */
    company: {
        name: 'Bombas Ideal S.A.',
        founded: 1902,
        phone: '+34 93 652 53 66',
        email: 'info@bombasideal.com',
        address: 'Polígono Industrial Can Salvatella',
        city: 'Barberà del Vallès',
        postalCode: '08210',
        country: 'España',
    },
    
    /**
     * URLs y endpoints
     */
    urls: {
        base: 'https://mutenros.github.io/BI',
        api: null, // No hay API actualmente
        catalogs: '/assets/docs/',
        images: '/assets/images/',
    },
    
    /**
     * Configuración del slider del hero
     */
    slider: {
        autoplay: true,
        interval: 6000,        // ms entre slides
        transitionDuration: 800, // ms de transición
        pauseOnHover: true,
    },
    
    /**
     * Configuración de navegación
     */
    navigation: {
        scrollThreshold: 100,   // px para activar navbar sticky
        mobileBreakpoint: 768,  // px para menú móvil
        hideTopBarOnScroll: true,
    },
    
    /**
     * Configuración de animaciones
     */
    animations: {
        enabled: true,
        duration: 300,          // ms duración base
        easing: 'ease-out',
        observerThreshold: 0.1, // % visible para trigger
    },
    
    /**
     * Configuración del sistema BIPS
     */
    bips: {
        resultsPerPage: 12,
        defaultView: 'grid',    // 'grid' o 'list'
        showMatchPercentage: true,
    },
    
    /**
     * Códigos secretos (Easter eggs)
     */
    secrets: {
        konamiCode: [
            'ArrowUp', 'ArrowUp',
            'ArrowDown', 'ArrowDown',
            'ArrowLeft', 'ArrowRight',
            'ArrowLeft', 'ArrowRight',
            'b', 'a'
        ],
        konamiRedirect: 'https://mutenros.github.io/?m=1&d=1',
    },
    
    /**
     * Breakpoints (deben coincidir con CSS)
     */
    breakpoints: {
        sm: 640,
        md: 768,
        lg: 1024,
        xl: 1280,
        '2xl': 1536,
    },
};

/**
 * Detecta si el dispositivo es móvil
 * @returns {boolean}
 */
export function isMobile() {
    return window.innerWidth < CONFIG.breakpoints.md;
}

/**
 * Detecta si el usuario prefiere movimiento reducido
 * @returns {boolean}
 */
export function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/**
 * Devuelve la duración de animación apropiada
 * @returns {number} - Duración en ms (0 si reduced motion)
 */
export function getAnimationDuration() {
    if (!CONFIG.animations.enabled || prefersReducedMotion()) {
        return 0;
    }
    return CONFIG.animations.duration;
}

export default CONFIG;
