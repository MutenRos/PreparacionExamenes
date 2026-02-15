/**
 * ==========================================================================
 * MUTENROS Portfolio - Configuration
 * ==========================================================================
 * 
 * Central configuration file for the portfolio.
 * Contains all configurable values, API endpoints, and settings.
 * 
 * @author Dario (MutenRos)
 * @version 2.0.0
 * @license MIT
 * ==========================================================================
 */

const CONFIG = {
    /**
     * GitHub Configuration
     * Settings for GitHub API integration
     */
    github: {
        username: 'MutenRos',
        apiBaseUrl: 'https://api.github.com',
        reposPerPage: 30,
        sortBy: 'updated',
        
        // Repository exclusions (won't appear in projects)
        excludeRepos: [
            'MutenRos.github.io' // Exclude portfolio itself
        ],
        
        // Exclude forked repositories
        excludeForks: true
    },
    
    /**
     * Private Projects
     * Projects with private code but public demos (GitHub Pages)
     * These are displayed alongside public repos
     */
    privateProjects: [
        {
            name: 'Tedeer',
            description: 'Mi proyecto principal. Plataforma completa de gestion y servicios.',
            language: 'Python',
            homepage: 'http://tedeer.duckdns.org:8001/',
            icon: 'fa-solid fa-leaf'
        },
        {
            name: 'Bombas Ideal',
            description: 'Web corporativa para empresa lider en bombas hidraulicas. Catalogo de productos, selector BIPS y gestion empresarial.',
            language: 'HTML',
            homepage: 'https://mutenros.github.io/BI',
            icon: 'fa-solid fa-droplet'
        },
        {
            name: 'Bombas Asoin',
            description: 'Tienda online de bombas de agua para riego, abastecimiento, achique y piscinas. Sistema de carrito integrado.',
            language: 'HTML',
            homepage: 'https://mutenros.github.io/BA',
            icon: 'fa-solid fa-cart-shopping'
        },
        {
            name: 'Bombas Bloch',
            description: 'Web corporativa para fabricante de sistemas de bombeo desde 1915. Catalogo, tienda y descargas tecnicas.',
            language: 'HTML',
            homepage: 'https://mutenros.github.io/BB',
            icon: 'fa-solid fa-industry'
        },
        {
            name: 'Cuevas MotorSport',
            description: 'Servicio de grua 24/7, alquiler de vehiculos deportivos y plataformas portacoches.',
            language: 'JavaScript',
            homepage: 'https://mutenros.github.io/CuevasMotorSport',
            icon: 'fa-solid fa-car'
        },
        {
            name: 'Espectaculos Dani',
            description: 'Web de entretenimiento y espectaculos. Eventos, shows y servicios de animacion.',
            language: 'HTML',
            homepage: 'https://mutenros.github.io/Espectaculos-Dani',
            icon: 'fa-solid fa-masks-theater'
        }
    ],
    
    /**
     * Matrix Easter Egg Doors
     * Configuration for the Matrix-themed easter egg
     */
    matrixDoors: [
        { name: '???', url: null, color: '#ff0000', mystery: true, desc: '' },
        { name: 'Tedeer', url: 'http://tedeer.duckdns.org:8001/', color: '#00ff41', desc: 'Mi proyecto principal.' },
        { name: 'Bombas Ideal', url: 'https://mutenros.github.io/BI', color: '#00aaff', desc: 'Catalogo de bombas hidraulicas.' },
        { name: 'Bombas Asoin', url: 'https://mutenros.github.io/BA', color: '#00ff88', desc: 'Tienda online de bombas.' },
        { name: 'Bombas Bloch', url: 'https://mutenros.github.io/BB', color: '#ff6600', desc: 'Fabricante desde 1915.' },
        { name: 'CuevasMotor', url: 'https://mutenros.github.io/CuevasMotorSport', color: '#ff0066', desc: 'Taller y grua 24 horas.' },
        { name: 'Espectaculos', url: 'https://mutenros.github.io/Espectaculos-Dani', color: '#aa00ff', desc: 'Shows y animacion.' },
        { name: 'Arraez', url: 'https://mutenros.github.io/Arraez-Portfolio', color: '#ffaa00', desc: 'Portfolio anterior.' },
        { name: 'Excusas', url: 'https://mutenros.github.io/Generador-de-Excusas-Premium', color: '#00ffaa', desc: 'Generador de excusas.' },
        { name: 'MenuSpreader', url: 'https://mutenros.github.io/MenuSpreader', color: '#ff00aa', desc: 'Gestor de menus.' },
        { name: 'Tokenizer', url: 'https://mutenros.github.io/TokenMinimizer', color: '#aaff00', desc: 'Optimizador de tokens.' }
    ],
    
    /**
     * Language Icons Mapping
     * Maps programming languages to Font Awesome icons
     */
    languageIcons: {
        'JavaScript': 'fa-brands fa-js',
        'TypeScript': 'fa-brands fa-js',
        'Python': 'fa-brands fa-python',
        'HTML': 'fa-brands fa-html5',
        'CSS': 'fa-brands fa-css3-alt',
        'Java': 'fa-brands fa-java',
        'C#': 'fa-solid fa-code',
        'C++': 'fa-solid fa-code',
        'Ruby': 'fa-solid fa-gem',
        'Go': 'fa-brands fa-golang',
        'Rust': 'fa-brands fa-rust',
        'PHP': 'fa-brands fa-php',
        'Swift': 'fa-brands fa-swift',
        'Kotlin': 'fa-solid fa-k',
        'default': 'fa-solid fa-folder'
    },
    
    /**
     * Animation Settings
     */
    animations: {
        starsCount: 100,
        parallaxSunSpeed: 0.3,
        parallaxMountainSpeed: 0.2
    },
    
    /**
     * Contact Information
     */
    contact: {
        email: 'tu@email.com',
        github: 'https://github.com/MutenRos',
        linkedin: 'https://linkedin.com'
    },
    
    /**
     * SEO & Meta
     */
    meta: {
        title: 'MUTENROS // Portfolio',
        description: 'Portfolio de Dario (MutenRos) - Desarrollador Web Full Stack',
        author: 'Dario (MutenRos)',
        year: new Date().getFullYear()
    }
};

// Freeze configuration to prevent accidental modifications
Object.freeze(CONFIG);
Object.freeze(CONFIG.github);
Object.freeze(CONFIG.languageIcons);
Object.freeze(CONFIG.animations);
Object.freeze(CONFIG.contact);
Object.freeze(CONFIG.meta);

export default CONFIG;
