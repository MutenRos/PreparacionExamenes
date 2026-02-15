/**
 * ==========================================================================
 * MUTENROS Portfolio - Main Application Entry Point
 * ==========================================================================
 * 
 * This is the main JavaScript file that initializes all modules
 * and coordinates the portfolio application.
 * 
 * @author Dario (MutenRos)
 * @version 2.0.0
 * @license MIT
 * 
 * Modules:
 * - Background Effects (stars, parallax)
 * - Navigation (smooth scroll, active section)
 * - Projects (GitHub API integration)
 * - Matrix Easter Egg (Konami code)
 * ==========================================================================
 */

import CONFIG from './config.js';
import backgroundEffects from './modules/background.js';
import navigation from './modules/navigation.js';
import githubProjects from './modules/projects.js';
import matrixEasterEgg from './modules/matrix-easter-egg.js';

/**
 * Portfolio Application Class
 * Main application controller that initializes and coordinates all modules
 */
class PortfolioApp {
    /**
     * Create portfolio application instance
     */
    constructor() {
        this.isInitialized = false;
        this.modules = {
            background: backgroundEffects,
            navigation: navigation,
            projects: githubProjects,
            easterEgg: matrixEasterEgg
        };
    }
    
    /**
     * Initialize the portfolio application
     * Called when DOM is ready
     */
    async init() {
        if (this.isInitialized) {
            console.warn('[PortfolioApp] Already initialized');
            return;
        }
        
        console.log('[PortfolioApp] Initializing...');
        console.log(`[PortfolioApp] Version ${CONFIG.meta.author}`);
        
        try {
            // Initialize all modules
            this.initBackground();
            this.initNavigation();
            await this.initProjects();
            this.initEasterEgg();
            
            this.isInitialized = true;
            console.log('[PortfolioApp] Initialization complete');
            
            // Log easter egg hint (barely visible)
            console.log('%c↑↑↓↓←→←→BA', 'color: #111; font-size: 1px;');
            
        } catch (error) {
            console.error('[PortfolioApp] Initialization error:', error);
        }
    }
    
    /**
     * Initialize background effects module
     */
    initBackground() {
        try {
            this.modules.background.init();
        } catch (error) {
            console.error('[PortfolioApp] Background init error:', error);
        }
    }
    
    /**
     * Initialize navigation module
     */
    initNavigation() {
        try {
            this.modules.navigation.init();
        } catch (error) {
            console.error('[PortfolioApp] Navigation init error:', error);
        }
    }
    
    /**
     * Initialize projects module (async - fetches from API)
     */
    async initProjects() {
        try {
            await this.modules.projects.init('#projects-grid');
        } catch (error) {
            console.error('[PortfolioApp] Projects init error:', error);
        }
    }
    
    /**
     * Initialize easter egg module
     */
    initEasterEgg() {
        try {
            this.modules.easterEgg.init();
        } catch (error) {
            console.error('[PortfolioApp] Easter egg init error:', error);
        }
    }
    
    /**
     * Cleanup and destroy all modules
     */
    destroy() {
        Object.values(this.modules).forEach(module => {
            if (typeof module.destroy === 'function') {
                module.destroy();
            }
        });
        this.isInitialized = false;
        console.log('[PortfolioApp] Destroyed');
    }
}

// Create application instance
const app = new PortfolioApp();

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => app.init());
} else {
    // DOM already loaded
    app.init();
}

// Export for debugging/testing
export default app;
export { PortfolioApp };
