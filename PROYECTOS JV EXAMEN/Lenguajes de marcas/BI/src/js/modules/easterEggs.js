/**
 * =============================================================================
 * BOMBAS IDEAL - Easter Eggs Module
 * =============================================================================
 * 
 * @description  Funcionalidades ocultas y easter eggs. Incluye el código
 *               Konami y otros secretos.
 * 
 * @author       Bombas Ideal Development Team
 * @version      2.0.0
 * @module       easterEggs
 */

import { CONFIG } from '../config.js';

/* =========================================================================
 * STATE
 * ========================================================================= */

/** @type {string[]} Secuencia actual de teclas */
let currentSequence = [];


/* =========================================================================
 * PRIVATE FUNCTIONS
 * ========================================================================= */

/**
 * Maneja las pulsaciones de tecla para detectar el código Konami
 * @private
 * @param {KeyboardEvent} event
 */
function handleKeyDown(event) {
    const { konamiCode, konamiRedirect } = CONFIG.secrets;
    
    // Añadir tecla a la secuencia
    currentSequence.push(event.key);
    
    // Mantener solo las últimas N teclas (longitud del código)
    if (currentSequence.length > konamiCode.length) {
        currentSequence.shift();
    }
    
    // Verificar si coincide con el código Konami
    const isMatch = currentSequence.every((key, index) => key === konamiCode[index]);
    
    if (isMatch && currentSequence.length === konamiCode.length) {
        activateKonamiCode();
    }
}

/**
 * Activa el easter egg del código Konami
 * @private
 */
function activateKonamiCode() {
    console.log('🎮 Konami Code Activated!');
    
    // Crear efecto visual antes de redirigir
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        inset: 0;
        background: black;
        z-index: 99999;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.5s ease;
    `;
    
    overlay.innerHTML = `
        <div style="
            color: #00ff00;
            font-family: monospace;
            font-size: 2rem;
            text-align: center;
            animation: glitch 0.5s ease-in-out;
        ">
            <p>ACCESS GRANTED</p>
            <p style="font-size: 1rem; margin-top: 1rem;">Entering the Matrix...</p>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    // Trigger fade in
    requestAnimationFrame(() => {
        overlay.style.opacity = '1';
    });
    
    // Redirigir después de la animación
    setTimeout(() => {
        window.location.href = CONFIG.secrets.konamiRedirect;
    }, 1500);
    
    // Resetear secuencia
    currentSequence = [];
}


/* =========================================================================
 * PUBLIC API
 * ========================================================================= */

/**
 * Inicializa el módulo de easter eggs
 */
export function init() {
    // Listener para código Konami
    document.addEventListener('keydown', handleKeyDown);
    
    console.log('Easter Eggs module initialized (secrets await...)');
}

/**
 * Destruye el módulo y limpia listeners
 */
export function destroy() {
    document.removeEventListener('keydown', handleKeyDown);
    currentSequence = [];
}

export default {
    init,
    destroy,
};
