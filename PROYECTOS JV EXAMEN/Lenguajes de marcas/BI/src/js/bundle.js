/**
 * =============================================================================
 * BOMBAS IDEAL - Bundle Entry Point
 * =============================================================================
 * 
 * @description  Punto de entrada principal que expone los módulos en el
 *               ámbito global para compatibilidad con HTML existente.
 *               Este archivo permite una migración gradual a ES modules.
 * 
 * @author       Bombas Ideal Development Team
 * @version      4.1.0
 * 
 * USO:
 * <script type="module" src="src/js/bundle.js"></script>
 * 
 * Después puedes usar:
 * - window.BI.init() para inicializar todo
 * - window.BIPS.search() para buscar bombas
 */

// ============================================================================
// IMPORTS
// ============================================================================

import * as Utils from './modules/utils.js';
import * as Navigation from './modules/navigation.js';
import * as Slider from './modules/slider.js';
import * as Animations from './modules/animations.js';
import * as ScrollTop from './modules/scrollTop.js';
import * as Modals from './modules/modals.js';
import * as EasterEggs from './modules/easterEggs.js';
import Config from './config.js';

// BIPS modules (solo si existen los elementos)
let BIPS = null;

// ============================================================================
// INITIALIZATION
// ============================================================================

/**
 * Inicializa todos los módulos de la página principal
 */
function initMainSite() {
    // Preloader
    const preloader = document.getElementById('preloader');
    if (preloader) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                preloader.classList.add('hidden');
                setTimeout(() => preloader.remove(), 500);
            }, 500);
        });
    }
    
    // Navegación
    Navigation.init();
    
    // Slider del hero
    Slider.init();
    
    // Animaciones al scroll
    Animations.init();
    
    // Botón volver arriba
    ScrollTop.init();
    
    // Modales
    Modals.init();
    
    // Easter eggs
    EasterEggs.init();
    
    // Cookies
    initCookies();
    
    console.log(`
    ╔═══════════════════════════════════════════════════════════╗
    ║                 🔵 BOMBAS IDEAL S.A. 🔵                  ║
    ║                                                           ║
    ║        ███████╗██╗██████╗ ███████╗ █████╗ ██╗            ║
    ║        ██╔════╝██║██╔══██╗██╔════╝██╔══██╗██║            ║
    ║        █████╗  ██║██║  ██║█████╗  ███████║██║            ║
    ║        ██╔══╝  ██║██║  ██║██╔══╝  ██╔══██║██║            ║
    ║        ██║     ██║██████╔╝███████╗██║  ██║███████╗       ║
    ║        ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝       ║
    ║                                                           ║
    ║   Fabricantes de bombas de agua desde 1902                ║
    ║   www.bombasideal.com | v4.1.0                            ║
    ╚═══════════════════════════════════════════════════════════╝
    `);
}

/**
 * Inicializa el banner de cookies
 */
function initCookies() {
    const banner = document.getElementById('cookie-banner');
    const acceptBtn = document.getElementById('accept-cookies');
    const configBtn = document.getElementById('config-cookies');
    
    if (!banner) return;
    
    // Verificar si ya aceptó
    if (localStorage.getItem('cookies_accepted')) {
        banner.style.display = 'none';
        return;
    }
    
    // Mostrar banner
    setTimeout(() => banner.classList.add('visible'), 2000);
    
    acceptBtn?.addEventListener('click', () => {
        localStorage.setItem('cookies_accepted', 'true');
        banner.classList.remove('visible');
    });
    
    configBtn?.addEventListener('click', () => {
        // TODO: Implementar modal de configuración
        console.log('Cookie config clicked');
    });
}

/**
 * Inicializa la página BIPS
 */
async function initBIPS() {
    try {
        const BIPSModule = await import('./bips/index.js');
        BIPS = BIPSModule.default;
        BIPS.init();
        
        // Exponer globalmente
        window.BIPS = BIPS;
        
    } catch (error) {
        console.error('Error loading BIPS:', error);
    }
}

// ============================================================================
// AUTO-INIT
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // Detectar qué página es
    const isBIPSPage = document.body.classList.contains('bips-page');
    
    if (isBIPSPage) {
        initBIPS();
    } else {
        initMainSite();
    }
});

// ============================================================================
// GLOBAL EXPORTS
// ============================================================================

/**
 * API global para la página principal
 */
window.BI = {
    init: initMainSite,
    Utils,
    Navigation,
    Slider,
    Animations,
    ScrollTop,
    Modals,
    EasterEggs,
    Config,
    version: '4.1.0',
};

// Informar que está listo
window.dispatchEvent(new CustomEvent('bi:ready', { detail: window.BI }));
