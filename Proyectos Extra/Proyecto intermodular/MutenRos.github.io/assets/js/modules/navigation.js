/**
 * ==========================================================================
 * MUTENROS Portfolio - Navigation Module
 * ==========================================================================
 * 
 * Handles navigation functionality:
 * - Smooth scrolling for anchor links
 * - Active section highlighting
 * - Mobile menu toggle (optional)
 * 
 * @author Dario (MutenRos)
 * @version 2.0.0
 * @license MIT
 * ==========================================================================
 */

import { smoothScrollTo, throttle, isInViewport } from './utils.js';

/**
 * Navigation Class
 * Manages all navigation-related functionality
 */
class Navigation {
    /**
     * Initialize navigation
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        this.navLinks = null;
        this.sections = null;
        this.header = null;
        
        this.options = {
            headerOffset: options.headerOffset || 100,
            activeClass: options.activeClass || 'is-active',
            scrollThreshold: options.scrollThreshold || 0.3
        };
        
        this.isInitialized = false;
    }
    
    /**
     * Initialize navigation functionality
     */
    init() {
        if (this.isInitialized) return;
        
        this.navLinks = document.querySelectorAll('.header__nav-link');
        this.sections = document.querySelectorAll('section[id]');
        this.header = document.querySelector('.header');
        
        this.bindEvents();
        this.initScrollSpy();
        
        this.isInitialized = true;
        console.log('[Navigation] Initialized');
    }
    
    /**
     * Bind click events to navigation links
     */
    bindEvents() {
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => this.handleNavClick(e));
        });
        
        // CTA button scroll (if exists)
        const ctaButton = document.querySelector('.hero__cta .btn');
        if (ctaButton) {
            ctaButton.addEventListener('click', (e) => {
                e.preventDefault();
                const target = ctaButton.getAttribute('data-scroll-to') || '#projects';
                smoothScrollTo(target, this.options.headerOffset);
            });
        }
    }
    
    /**
     * Handle navigation link click
     * @param {Event} e - Click event
     */
    handleNavClick(e) {
        e.preventDefault();
        const href = e.currentTarget.getAttribute('href');
        
        if (href && href.startsWith('#')) {
            smoothScrollTo(href, this.options.headerOffset);
            
            // Update URL hash without scrolling
            history.pushState(null, null, href);
        }
    }
    
    /**
     * Initialize scroll spy to highlight active section
     */
    initScrollSpy() {
        const handleScroll = throttle(() => {
            this.updateActiveSection();
        }, 100);
        
        window.addEventListener('scroll', handleScroll, { passive: true });
        
        // Initial check
        this.updateActiveSection();
    }
    
    /**
     * Update active navigation link based on scroll position
     */
    updateActiveSection() {
        let currentSection = '';
        
        this.sections.forEach(section => {
            const sectionTop = section.offsetTop - this.options.headerOffset - 50;
            const sectionHeight = section.offsetHeight;
            
            if (window.pageYOffset >= sectionTop && 
                window.pageYOffset < sectionTop + sectionHeight) {
                currentSection = section.getAttribute('id');
            }
        });
        
        // Update active class on nav links
        this.navLinks.forEach(link => {
            link.classList.remove(this.options.activeClass);
            
            const href = link.getAttribute('href');
            if (href === `#${currentSection}`) {
                link.classList.add(this.options.activeClass);
            }
        });
    }
    
    /**
     * Cleanup and remove event listeners
     */
    destroy() {
        this.navLinks = null;
        this.sections = null;
        this.header = null;
        this.isInitialized = false;
    }
}

// Create singleton instance
const navigation = new Navigation();

export default navigation;
export { Navigation };
