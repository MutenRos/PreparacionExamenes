/**
 * =============================================================================
 * BOMBAS IDEAL - Main Application Entry Point
 * =============================================================================
 * 
 * @description  Punto de entrada principal de la aplicación JavaScript.
 *               Importa e inicializa todos los módulos necesarios.
 * 
 * @author       Bombas Ideal Development Team
 * @version      2.0.0
 * @license      Proprietary - Bombas Ideal S.A.
 * 
 * ARQUITECTURA:
 * - config.js:           Configuración centralizada
 * - modules/utils.js:    Utilidades reutilizables
 * - modules/navigation.js: Navegación y menú móvil
 * - modules/slider.js:   Hero slider
 * - modules/animations.js: Animaciones de entrada
 * - modules/scrollTop.js: Botón scroll to top
 * - modules/modals.js:   Sistema de modales
 * - modules/easterEggs.js: Easter eggs ocultos
 * =============================================================================
 */

import { onReady } from './modules/utils.js';
import CONFIG from './config.js';

// Módulos
import * as Navigation from './modules/navigation.js';
import * as Slider from './modules/slider.js';
import * as Animations from './modules/animations.js';
import * as ScrollTop from './modules/scrollTop.js';
import * as Modals from './modules/modals.js';
import * as EasterEggs from './modules/easterEggs.js';


/* =========================================================================
 * INITIALIZATION
 * ========================================================================= */

/**
 * Inicializa todos los módulos de la aplicación
 */
function initApp() {
    console.log(`%c
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║          🔵 BOMBAS IDEAL S.A. 🔵            ║
    ║                                              ║
    ║      Fabricantes de bombas desde 1902        ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    `, 'color: #0a4f8c; font-weight: bold;');
    
    console.log('%c v2.0.0 | https://bombasideal.com', 'color: #00c8c8;');
    console.log('');
    
    // Inicializar módulos en orden
    try {
        Navigation.init();
        Slider.init();
        Animations.init();
        ScrollTop.init();
        Modals.init();
        EasterEggs.init();
        
        console.log('%c✓ All modules initialized successfully', 'color: #22c55e;');
    } catch (error) {
        console.error('Error initializing modules:', error);
    }
}

/**
 * Ejecutar cuando el DOM esté listo
 */
onReady(initApp);


/* =========================================================================
 * EXPORTS
 * =========================================================================
 * Exportamos los módulos para uso externo si es necesario
 */

export {
    CONFIG,
    Navigation,
    Slider,
    Animations,
    ScrollTop,
    Modals,
    EasterEggs,
};

// También exponemos en window para debugging y uso legacy
if (typeof window !== 'undefined') {
    window.BI = {
        CONFIG,
        Navigation,
        Slider,
        Animations,
        ScrollTop,
        Modals,
        version: '2.0.0',
    };
}
