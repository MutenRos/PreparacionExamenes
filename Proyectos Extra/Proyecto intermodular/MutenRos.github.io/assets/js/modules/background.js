/**
 * ==========================================================================
 * MUTENROS Portfolio - Background Effects Module
 * ==========================================================================
 * 
 * Handles all animated background effects:
 * - Dynamic star generation
 * - Parallax scrolling effects
 * 
 * @author Dario (MutenRos)
 * @version 2.0.0
 * @license MIT
 * ==========================================================================
 */

import CONFIG from '../config.js';
import { randomRange, throttle } from './utils.js';

/**
 * BackgroundEffects Class
 * Manages all background visual effects
 */
class BackgroundEffects {
    /**
     * Initialize background effects
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        this.starsContainer = null;
        this.sunElement = null;
        this.mountainsElement = null;
        
        this.options = {
            starsCount: options.starsCount || CONFIG.animations.starsCount,
            parallaxSunSpeed: options.parallaxSunSpeed || CONFIG.animations.parallaxSunSpeed,
            parallaxMountainSpeed: options.parallaxMountainSpeed || CONFIG.animations.parallaxMountainSpeed
        };
        
        this.isInitialized = false;
    }
    
    /**
     * Initialize all background effects
     */
    init() {
        if (this.isInitialized) return;
        
        this.starsContainer = document.getElementById('stars');
        this.sunElement = document.querySelector('.bg-sun');
        this.mountainsElement = document.querySelector('.bg-mountains');
        
        this.generateStars();
        this.initParallax();
        
        this.isInitialized = true;
        console.log('[BackgroundEffects] Initialized');
    }
    
    /**
     * Generate twinkling stars dynamically
     * Creates star elements with random positions and animation delays
     */
    generateStars() {
        if (!this.starsContainer) {
            console.warn('[BackgroundEffects] Stars container not found');
            return;
        }
        
        // Clear existing stars
        this.starsContainer.innerHTML = '';
        
        // Create document fragment for better performance
        const fragment = document.createDocumentFragment();
        
        for (let i = 0; i < this.options.starsCount; i++) {
            const star = document.createElement('div');
            star.className = 'bg-star';
            
            // Random positioning
            star.style.left = `${randomRange(0, 100)}%`;
            star.style.top = `${randomRange(0, 100)}%`;
            
            // Random animation delay for staggered twinkling
            star.style.animationDelay = `${randomRange(0, 2)}s`;
            
            // Random size variation (1-3px)
            const size = randomRange(1, 3);
            star.style.width = `${size}px`;
            star.style.height = `${size}px`;
            
            fragment.appendChild(star);
        }
        
        this.starsContainer.appendChild(fragment);
        console.log(`[BackgroundEffects] Generated ${this.options.starsCount} stars`);
    }
    
    /**
     * Initialize parallax scrolling effect
     * Sun and mountains move at different speeds on scroll
     */
    initParallax() {
        // Use throttled scroll handler for performance
        const handleScroll = throttle(() => {
            this.updateParallax();
        }, 16); // ~60fps
        
        window.addEventListener('scroll', handleScroll, { passive: true });
    }
    
    /**
     * Update parallax positions based on scroll
     */
    updateParallax() {
        const scrolled = window.pageYOffset;
        
        // Parallax sun movement
        if (this.sunElement) {
            const sunOffset = scrolled * this.options.parallaxSunSpeed;
            this.sunElement.style.transform = `translateX(-50%) translateY(${sunOffset}px)`;
        }
        
        // Parallax mountains movement (slower than sun)
        if (this.mountainsElement) {
            const mountainOffset = scrolled * this.options.parallaxMountainSpeed;
            this.mountainsElement.style.transform = `translateY(${mountainOffset}px)`;
        }
    }
    
    /**
     * Cleanup and remove event listeners
     */
    destroy() {
        // Stars will be cleaned up when container is removed
        this.starsContainer = null;
        this.sunElement = null;
        this.mountainsElement = null;
        this.isInitialized = false;
    }
}

// Create singleton instance
const backgroundEffects = new BackgroundEffects();

export default backgroundEffects;
export { BackgroundEffects };
