/**
 * =============================================================================
 * BOMBAS IDEAL - Slider Module
 * =============================================================================
 * 
 * @description  Componente de slider/carrusel para el hero principal.
 *               Soporta autoplay, controles manuales, indicadores,
 *               swipe en móvil y pause on hover.
 * 
 * @author       Bombas Ideal Development Team
 * @version      2.0.0
 * @module       slider
 */

import { $, $$, addClass, removeClass, hasClass } from './utils.js';
import { CONFIG, prefersReducedMotion } from '../config.js';

/* =========================================================================
 * STATE
 * ========================================================================= */

/** @type {Object} Estado interno del slider */
const state = {
    currentIndex: 0,
    slidesCount: 0,
    isPlaying: false,
    intervalId: null,
    touchStartX: 0,
    touchEndX: 0,
};


/* =========================================================================
 * DOM ELEMENTS
 * ========================================================================= */

/** @type {Object} Referencias a elementos del DOM */
let elements = {
    container: null,
    slides: [],
    prevBtn: null,
    nextBtn: null,
    indicators: null,
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
        container: $('.hero-slider'),
        slides: $$('.slide'),
        prevBtn: $('.slider-btn-prev'),
        nextBtn: $('.slider-btn-next'),
        indicators: $$('.indicator'),
    };
    
    state.slidesCount = elements.slides.length;
}

/**
 * Muestra un slide específico
 * @private
 * @param {number} index - Índice del slide a mostrar
 */
function showSlide(index) {
    // Validar índice
    if (index < 0) {
        index = state.slidesCount - 1;
    } else if (index >= state.slidesCount) {
        index = 0;
    }
    
    // Actualizar estado
    state.currentIndex = index;
    
    // Actualizar slides
    elements.slides.forEach((slide, i) => {
        if (i === index) {
            addClass(slide, 'active');
        } else {
            removeClass(slide, 'active');
        }
    });
    
    // Actualizar indicadores
    elements.indicators.forEach((indicator, i) => {
        if (i === index) {
            addClass(indicator, 'active');
        } else {
            removeClass(indicator, 'active');
        }
    });
}

/**
 * Avanza al siguiente slide
 * @private
 */
function nextSlide() {
    showSlide(state.currentIndex + 1);
}

/**
 * Retrocede al slide anterior
 * @private
 */
function prevSlide() {
    showSlide(state.currentIndex - 1);
}

/**
 * Inicia el autoplay
 * @private
 */
function startAutoplay() {
    if (state.isPlaying || prefersReducedMotion()) return;
    
    const { interval } = CONFIG.slider;
    
    state.isPlaying = true;
    state.intervalId = setInterval(nextSlide, interval);
}

/**
 * Detiene el autoplay
 * @private
 */
function stopAutoplay() {
    if (!state.isPlaying) return;
    
    state.isPlaying = false;
    clearInterval(state.intervalId);
    state.intervalId = null;
}

/**
 * Maneja el inicio de touch
 * @private
 * @param {TouchEvent} event
 */
function handleTouchStart(event) {
    state.touchStartX = event.changedTouches[0].screenX;
}

/**
 * Maneja el final de touch (swipe)
 * @private
 * @param {TouchEvent} event
 */
function handleTouchEnd(event) {
    state.touchEndX = event.changedTouches[0].screenX;
    handleSwipe();
}

/**
 * Procesa el gesto de swipe
 * @private
 */
function handleSwipe() {
    const threshold = 50; // px mínimos para considerar swipe
    const diff = state.touchStartX - state.touchEndX;
    
    if (Math.abs(diff) < threshold) return;
    
    if (diff > 0) {
        // Swipe izquierda -> siguiente
        nextSlide();
    } else {
        // Swipe derecha -> anterior
        prevSlide();
    }
    
    // Resetear autoplay
    if (CONFIG.slider.autoplay) {
        stopAutoplay();
        startAutoplay();
    }
}

/**
 * Maneja el hover sobre el slider
 * @private
 */
function handleMouseEnter() {
    if (CONFIG.slider.pauseOnHover && state.isPlaying) {
        stopAutoplay();
    }
}

/**
 * Maneja cuando el mouse sale del slider
 * @private
 */
function handleMouseLeave() {
    if (CONFIG.slider.autoplay && !state.isPlaying) {
        startAutoplay();
    }
}

/**
 * Maneja el click en un indicador
 * @private
 * @param {number} index - Índice del indicador
 */
function handleIndicatorClick(index) {
    showSlide(index);
    
    // Resetear autoplay
    if (CONFIG.slider.autoplay) {
        stopAutoplay();
        startAutoplay();
    }
}

/**
 * Maneja las teclas de navegación
 * @private
 * @param {KeyboardEvent} event
 */
function handleKeyDown(event) {
    // Solo si el slider está en foco
    if (!elements.container.contains(document.activeElement)) return;
    
    switch (event.key) {
        case 'ArrowLeft':
            prevSlide();
            break;
        case 'ArrowRight':
            nextSlide();
            break;
    }
}


/* =========================================================================
 * PUBLIC API
 * ========================================================================= */

/**
 * Inicializa el módulo del slider
 */
export function init() {
    cacheElements();
    
    // Verificar que existan slides
    if (state.slidesCount === 0) {
        console.warn('Slider: No slides found');
        return;
    }
    
    // Event listeners
    
    // Botones de navegación
    if (elements.prevBtn) {
        elements.prevBtn.addEventListener('click', () => {
            prevSlide();
            if (CONFIG.slider.autoplay) {
                stopAutoplay();
                startAutoplay();
            }
        });
    }
    
    if (elements.nextBtn) {
        elements.nextBtn.addEventListener('click', () => {
            nextSlide();
            if (CONFIG.slider.autoplay) {
                stopAutoplay();
                startAutoplay();
            }
        });
    }
    
    // Indicadores
    elements.indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => handleIndicatorClick(index));
    });
    
    // Touch/Swipe
    if (elements.container) {
        elements.container.addEventListener('touchstart', handleTouchStart, { passive: true });
        elements.container.addEventListener('touchend', handleTouchEnd, { passive: true });
        
        // Pause on hover
        if (CONFIG.slider.pauseOnHover) {
            elements.container.addEventListener('mouseenter', handleMouseEnter);
            elements.container.addEventListener('mouseleave', handleMouseLeave);
        }
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', handleKeyDown);
    
    // Estado inicial
    showSlide(0);
    
    // Iniciar autoplay si está configurado
    if (CONFIG.slider.autoplay) {
        startAutoplay();
    }
    
    console.log('Slider module initialized');
}

/**
 * Navega a un slide específico
 * @param {number} index - Índice del slide
 */
export function goTo(index) {
    showSlide(index);
}

/**
 * Avanza al siguiente slide
 */
export function next() {
    nextSlide();
}

/**
 * Retrocede al slide anterior
 */
export function prev() {
    prevSlide();
}

/**
 * Inicia el autoplay
 */
export function play() {
    if (CONFIG.slider.autoplay) {
        startAutoplay();
    }
}

/**
 * Pausa el autoplay
 */
export function pause() {
    stopAutoplay();
}

/**
 * Obtiene el índice del slide actual
 * @returns {number}
 */
export function getCurrentIndex() {
    return state.currentIndex;
}

/**
 * Obtiene el número total de slides
 * @returns {number}
 */
export function getSlidesCount() {
    return state.slidesCount;
}

export default {
    init,
    goTo,
    next,
    prev,
    play,
    pause,
    getCurrentIndex,
    getSlidesCount,
};
