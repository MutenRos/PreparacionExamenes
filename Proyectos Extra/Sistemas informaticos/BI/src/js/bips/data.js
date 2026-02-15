/**
 * =============================================================================
 * BOMBAS IDEAL - BIPS Data (Pump Series Database)
 * =============================================================================
 * 
 * @description  Base de datos de series de bombas basada en catálogos
 *               oficiales de Bombas Ideal. Solo se recomiendan series,
 *               el modelo exacto se determina consultando el catálogo.
 * 
 * @author       Bombas Ideal Development Team
 * @version      4.1.0
 * @module       bips/data
 * 
 * IMPORTANTE: Estos datos provienen de catálogos oficiales.
 * Para actualizaciones, consultar los PDFs de cada serie.
 */

/**
 * Sectores/aplicaciones disponibles
 * @constant {Object}
 */
export const SECTORS = {
    water: {
        id: 'water',
        name: 'Abastecimiento',
        icon: 'fas fa-tint',
        description: 'Suministro y distribución de agua potable'
    },
    building: {
        id: 'building',
        name: 'Edificación',
        icon: 'fas fa-building',
        description: 'Grupos de presión para edificios'
    },
    industrial: {
        id: 'industrial',
        name: 'Industrial',
        icon: 'fas fa-industry',
        description: 'Procesos industriales y refrigeración'
    },
    agriculture: {
        id: 'agriculture',
        name: 'Agricultura',
        icon: 'fas fa-leaf',
        description: 'Riego agrícola y sistemas de fertirrigación'
    },
    fire: {
        id: 'fire',
        name: 'Contra incendios',
        icon: 'fas fa-fire-extinguisher',
        description: 'Sistemas normalizados UNE y NFPA'
    },
    drainage: {
        id: 'drainage',
        name: 'Drenaje',
        icon: 'fas fa-water',
        description: 'Evacuación de aguas residuales'
    },
    pool: {
        id: 'pool',
        name: 'Piscinas',
        icon: 'fas fa-swimming-pool',
        description: 'Filtración y recirculación de piscinas'
    }
};

/**
 * Tipos de instalación
 * @constant {Object}
 */
export const INSTALLATION_TYPES = {
    surface: { id: 'surface', name: 'Superficie', icon: 'fas fa-box' },
    submersible: { id: 'submersible', name: 'Sumergible', icon: 'fas fa-water' },
    inline: { id: 'inline', name: 'In-Line', icon: 'fas fa-arrows-alt-v' }
};

/**
 * Materiales de construcción
 * @constant {Object}
 */
export const MATERIALS = {
    'cast-iron': { id: 'cast-iron', name: 'Fundición', icon: 'fas fa-cube' },
    'stainless': { id: 'stainless', name: 'Inox AISI 304', icon: 'fas fa-gem' },
    'stainless-316': { id: 'stainless-316', name: 'Inox AISI 316', icon: 'fas fa-gem' },
    'bronze': { id: 'bronze', name: 'Bronce', icon: 'fas fa-coins' },
    'plastic': { id: 'plastic', name: 'Plástico', icon: 'fas fa-recycle' }
};

/**
 * Base de datos de series de bombas
 * Datos extraídos de catálogos oficiales Bombas Ideal
 * @constant {Array}
 */
export const SERIES_DATABASE = [
    // ============================================
    // BOMBAS VERTICALES MULTICELULARES
    // ============================================
    
    {
        id: 'NXA',
        series: 'NXA',
        name: 'Serie NXA',
        type: 'Multicelular Vertical Compacta',
        description: 'Electrobombas verticales multicelulares de alta presión diseñadas para instalación "IN LINE". Acero inoxidable AISI 304.',
        flow: { min: 0.3, max: 20 },
        head: { min: 10, max: 100 },
        power: { min: 0.37, max: 7.5 },
        material: 'stainless',
        maxTemp: 120,
        rpm: 2900,
        connection: 'DN25-DN50',
        efficiency: 65,
        sectors: ['water', 'building', 'agriculture', 'fire'],
        installation: 'surface',
        phase: 'both',
        solids: 0,
        catalog: 'Catalogo-NXA-Multicelulares.pdf',
        productPage: 'productos/serie-nxa.html',
        image: 'assets/images/serie-nxa-new.jpg'
    },

    {
        id: 'VIPV',
        series: 'VIPV',
        name: 'Serie VIPV',
        type: 'Multicelular Vertical',
        description: 'Bomba centrífuga multicelular especialmente indicada para grupos de presión. Funcionamiento silencioso.',
        flow: { min: 1, max: 80 },
        head: { min: 10, max: 200 },
        power: { min: 0.37, max: 37 },
        material: 'stainless',
        maxTemp: 90,
        rpm: 2900,
        connection: 'DN40-DN100',
        efficiency: 72,
        sectors: ['water', 'industrial', 'building'],
        installation: 'surface',
        phase: 'three',
        solids: 0,
        catalog: 'Catalogo-VIPV-NX-NLX-NLV.pdf',
        productPage: 'productos/serie-vipv.html',
        image: 'assets/images/serie-vipv-new.jpg'
    },

    {
        id: 'VIPH',
        series: 'VIPH',
        name: 'Serie VIPH',
        type: 'Multicelular Horizontal',
        description: 'Bomba centrífuga multicelular horizontal de funcionamiento silencioso. Presión de servicio 11 bar máx.',
        flow: { min: 1, max: 120 },
        head: { min: 10, max: 250 },
        power: { min: 0.37, max: 55 },
        material: 'stainless',
        maxTemp: 90,
        rpm: 2900,
        connection: 'DN40-DN100',
        efficiency: 72,
        sectors: ['water', 'industrial', 'building'],
        installation: 'surface',
        phase: 'three',
        solids: 0,
        catalog: 'Catalogo-VIPV-NX-NLX-NLV.pdf',
        productPage: 'productos/serie-viph.html',
        image: 'assets/images/serie-viph-new.jpg'
    },

    {
        id: 'NLX',
        series: 'NLX',
        name: 'Serie NLX',
        type: 'Multicelular In Line AISI 316',
        description: 'Multicelulares verticales "In Line" en acero inoxidable AISI 316 para aguas limpias.',
        flow: { min: 0.5, max: 70 },
        head: { min: 10, max: 220 },
        power: { min: 0.55, max: 45 },
        material: 'stainless-316',
        maxTemp: 90,
        rpm: 2900,
        connection: 'DN32-DN80',
        efficiency: 70,
        sectors: ['water', 'industrial', 'building'],
        installation: 'inline',
        phase: 'three',
        solids: 0,
        catalog: 'Catalogo-VIPV-NX-NLX-NLV.pdf',
        productPage: 'productos/serie-nlx.html',
        image: 'assets/images/serie-nlx-new.jpg'
    },

    {
        id: 'NLV',
        series: 'NLV',
        name: 'Serie NLV',
        type: 'Multicelular In Line',
        description: 'Multicelulares verticales "In Line" para instalaciones de presión y climatización.',
        flow: { min: 1, max: 50 },
        head: { min: 10, max: 180 },
        power: { min: 0.37, max: 37 },
        material: 'stainless',
        maxTemp: 90,
        rpm: 2900,
        connection: 'DN32-DN80',
        efficiency: 70,
        sectors: ['water', 'building'],
        installation: 'inline',
        phase: 'three',
        solids: 0,
        catalog: 'Catalogo-VIPV-NX-NLX-NLV.pdf',
        productPage: 'productos/serie-nlv.html',
        image: 'assets/images/serie-nlv.jpg'
    },

    {
        id: 'APM',
        series: 'APM',
        name: 'Serie APM',
        type: 'Multicelular Alta Presión',
        description: 'Bombas centrífugas multicelulares de alta presión. Motores IE3.',
        flow: { min: 1, max: 120 },
        head: { min: 20, max: 250 },
        power: { min: 0.37, max: 45 },
        material: 'cast-iron',
        maxTemp: 80,
        rpm: 2900,
        connection: 'DN50-DN150',
        efficiency: 75,
        sectors: ['water', 'industrial', 'fire'],
        installation: 'surface',
        phase: 'three',
        solids: 0,
        catalog: 'Catalogo-APM.pdf',
        productPage: 'productos/serie-apm.html',
        image: 'assets/images/serie-apm.jpg'
    },

    // ============================================
    // BOMBAS HORIZONTALES
    // ============================================

    {
        id: 'CP',
        series: 'CP',
        name: 'Serie CP',
        type: 'Centrífuga Cámara Partida',
        description: 'Bombas centrífugas horizontales de cámara partida. Grandes caudales.',
        flow: { min: 50, max: 10000 },
        head: { min: 10, max: 200 },
        power: { min: 7.5, max: 500 },
        material: 'cast-iron',
        maxTemp: 100,
        rpm: 1450,
        connection: 'DN100-DN600',
        efficiency: 85,
        sectors: ['water', 'industrial', 'fire'],
        installation: 'surface',
        phase: 'three',
        solids: 0,
        catalog: 'Catalogo-CPH-Serie-CP.pdf',
        productPage: 'productos/serie-cp.html',
        image: 'assets/images/serie-cp-new.jpg'
    },

    {
        id: 'RN',
        series: 'RN',
        name: 'Serie RN',
        type: 'Centrífuga Aspiración Axial',
        description: 'Bombas centrífugas horizontales de aspiración axial. Construcción robusta. Motores IE3.',
        flow: { min: 5, max: 2500 },
        head: { min: 5, max: 160 },
        power: { min: 0.37, max: 315 },
        material: 'cast-iron',
        maxTemp: 90,
        rpm: 1450,
        connection: 'DN50-DN300',
        efficiency: 78,
        sectors: ['water', 'industrial', 'agriculture'],
        installation: 'surface',
        phase: 'three',
        solids: 0,
        catalog: 'Catalogo-RN.pdf',
        productPage: 'productos/serie-rn.html',
        image: 'assets/images/serie-rn.jpg'
    },

    {
        id: 'RNL',
        series: 'RNL',
        name: 'Serie RNL',
        type: 'Centrífuga In Line',
        description: 'Bombas verticales con aspiración horizontal "In-Line". Instalación en tubería.',
        flow: { min: 5, max: 1200 },
        head: { min: 5, max: 100 },
        power: { min: 0.55, max: 160 },
        material: 'cast-iron',
        maxTemp: 90,
        rpm: 1450,
        connection: 'DN50-DN300',
        efficiency: 78,
        sectors: ['water', 'building'],
        installation: 'inline',
        phase: 'three',
        solids: 0,
        catalog: 'Catalogo-RNL.pdf',
        productPage: 'productos/serie-rnl.html',
        image: 'assets/images/serie-rnl.jpg'
    },

    {
        id: 'RFXA',
        series: 'RFXA',
        name: 'Serie RFXA',
        type: 'Monobloc Inox EN 733',
        description: 'Electrobomba monobloc inoxidable con bomba normalizada EN 733. Industria alimentaria.',
        flow: { min: 2, max: 400 },
        head: { min: 5, max: 90 },
        power: { min: 0.55, max: 45 },
        material: 'stainless',
        maxTemp: 90,
        rpm: 2900,
        connection: 'DN32-DN150',
        efficiency: 72,
        sectors: ['water', 'industrial'],
        installation: 'surface',
        phase: 'three',
        solids: 0,
        catalog: 'Catalogo-RFXA.pdf',
        productPage: 'productos/serie-rfxa.html',
        image: 'assets/images/serie-rfxa.jpg'
    },

    // ============================================
    // BOMBAS AUTOASPIRANTES
    // ============================================

    {
        id: 'CEB',
        series: 'CEB',
        name: 'Serie CEB',
        type: 'Autoaspirante',
        description: 'Bombas centrífugas autoaspirantes para aguas residuales. Paso de sólidos hasta 76mm.',
        flow: { min: 5, max: 400 },
        head: { min: 10, max: 90 },
        power: { min: 1.5, max: 75 },
        material: 'cast-iron',
        maxTemp: 40,
        rpm: 1450,
        connection: 'DN50-DN200',
        efficiency: 55,
        sectors: ['agriculture', 'drainage', 'industrial'],
        installation: 'surface',
        phase: 'three',
        solids: 76,
        catalog: 'Catalogo-CEB-Autoaspirantes.pdf',
        productPage: 'productos/serie-ceb.html',
        image: 'assets/images/serie-ceb-new.jpg'
    },

    // ============================================
    // BOMBAS SUMERGIDAS
    // ============================================

    {
        id: 'SBS',
        series: 'SBS',
        name: 'Serie SBS',
        type: 'Sumergible Aguas Limpias',
        description: 'Electrobombas sumergibles para captación de aguas limpias en pozos de 4".',
        flow: { min: 0.5, max: 25 },
        head: { min: 10, max: 300 },
        power: { min: 0.37, max: 7.5 },
        material: 'stainless',
        maxTemp: 35,
        rpm: 2900,
        connection: 'DN25-DN50',
        efficiency: 65,
        sectors: ['water', 'agriculture', 'building'],
        installation: 'submersible',
        phase: 'both',
        solids: 0,
        catalog: 'Catalogo-SBS-Sumergibles.pdf',
        productPage: 'productos/serie-sbs.html',
        image: 'assets/images/serie-sbs.jpg'
    },

    {
        id: 'SD',
        series: 'SD',
        name: 'Serie SD',
        type: 'Sumergible Drenaje',
        description: 'Electrobombas sumergibles para drenaje de aguas limpias o ligeramente sucias.',
        flow: { min: 5, max: 80 },
        head: { min: 5, max: 30 },
        power: { min: 0.25, max: 3 },
        material: 'plastic',
        maxTemp: 35,
        rpm: 2900,
        connection: 'DN32-DN80',
        efficiency: 50,
        sectors: ['drainage', 'building'],
        installation: 'submersible',
        phase: 'single',
        solids: 35,
        catalog: 'Catalogo-SD-Drenaje.pdf',
        productPage: 'productos/serie-sd.html',
        image: 'assets/images/serie-sd.jpg'
    },

    {
        id: 'SDX',
        series: 'SDX',
        name: 'Serie SDX',
        type: 'Sumergible Drenaje Inox',
        description: 'Electrobombas sumergibles de drenaje en acero inoxidable. Alta resistencia.',
        flow: { min: 5, max: 100 },
        head: { min: 5, max: 35 },
        power: { min: 0.25, max: 3 },
        material: 'stainless',
        maxTemp: 40,
        rpm: 2900,
        connection: 'DN32-DN80',
        efficiency: 55,
        sectors: ['drainage', 'industrial'],
        installation: 'submersible',
        phase: 'single',
        solids: 35,
        catalog: 'Catalogo-SDX-Drenaje-Inox.pdf',
        productPage: 'productos/serie-sdx.html',
        image: 'assets/images/serie-sdx.jpg'
    },

    // ============================================
    // GRUPOS DOMÉSTICOS
    // ============================================

    {
        id: 'HYDRO-H',
        series: 'HYDRO-H',
        name: 'Hydro H',
        type: 'Grupo Doméstico Horizontal',
        description: 'Grupos de presión domésticos con bomba horizontal autoaspirante.',
        flow: { min: 1, max: 8 },
        head: { min: 20, max: 55 },
        power: { min: 0.37, max: 1.5 },
        material: 'cast-iron',
        maxTemp: 35,
        rpm: 2900,
        connection: 'DN25',
        efficiency: 45,
        sectors: ['building'],
        installation: 'surface',
        phase: 'single',
        solids: 0,
        catalog: 'Catalogo-Grupos-Domesticos.pdf',
        productPage: 'productos/hydro-h.html',
        image: 'assets/images/hydro-h.jpg'
    },

    {
        id: 'HYDRO-V',
        series: 'HYDRO-V',
        name: 'Hydro V',
        type: 'Grupo Doméstico Vertical',
        description: 'Grupos de presión domésticos con bomba multicelular vertical.',
        flow: { min: 1, max: 10 },
        head: { min: 20, max: 70 },
        power: { min: 0.37, max: 1.5 },
        material: 'stainless',
        maxTemp: 35,
        rpm: 2900,
        connection: 'DN25',
        efficiency: 55,
        sectors: ['building'],
        installation: 'surface',
        phase: 'single',
        solids: 0,
        catalog: 'Catalogo-Grupos-Domesticos.pdf',
        productPage: 'productos/hydro-v.html',
        image: 'assets/images/hydro-v.jpg'
    },

    // ============================================
    // CONTRA INCENDIOS
    // ============================================

    {
        id: 'UNE23500',
        series: 'UNE23500',
        name: 'Serie UNE 23500',
        type: 'Grupo Contra Incendios UNE',
        description: 'Grupos de presión contra incendios según norma UNE 23500.',
        flow: { min: 10, max: 500 },
        head: { min: 20, max: 150 },
        power: { min: 5.5, max: 132 },
        material: 'cast-iron',
        maxTemp: 40,
        rpm: 2900,
        connection: 'DN65-DN200',
        efficiency: 75,
        sectors: ['fire'],
        installation: 'surface',
        phase: 'three',
        solids: 0,
        catalog: 'Catalogo-Contraincendios-UNE.pdf',
        productPage: 'productos/serie-une23500.html',
        image: 'assets/images/serie-une23500.jpg'
    },

    {
        id: 'NFPA20',
        series: 'NFPA20',
        name: 'Serie NFPA 20',
        type: 'Grupo Contra Incendios NFPA',
        description: 'Grupos de presión contra incendios según norma americana NFPA 20.',
        flow: { min: 10, max: 1000 },
        head: { min: 20, max: 200 },
        power: { min: 5.5, max: 250 },
        material: 'cast-iron',
        maxTemp: 40,
        rpm: 1750,
        connection: 'DN65-DN300',
        efficiency: 80,
        sectors: ['fire'],
        installation: 'surface',
        phase: 'three',
        solids: 0,
        catalog: 'Catalogo-Contraincendios-NFPA.pdf',
        productPage: 'productos/serie-nfpa20.html',
        image: 'assets/images/serie-nfpa20.jpg'
    },

    // ============================================
    // VARIADORES DE VELOCIDAD
    // ============================================

    {
        id: 'VARIVIP',
        series: 'VARIVIP',
        name: 'VariVIP',
        type: 'Grupo con Variador',
        description: 'Grupos de presión con variador de velocidad integrado. Máxima eficiencia energética.',
        flow: { min: 1, max: 200 },
        head: { min: 20, max: 200 },
        power: { min: 0.75, max: 55 },
        material: 'stainless',
        maxTemp: 40,
        rpm: 2900,
        connection: 'DN40-DN100',
        efficiency: 80,
        sectors: ['water', 'building', 'industrial'],
        installation: 'surface',
        phase: 'three',
        solids: 0,
        catalog: 'Catalogo-VariVIP.pdf',
        productPage: 'productos/varivip.html',
        image: 'assets/images/varivip.jpg'
    }
];

/**
 * Obtiene una serie por su ID
 * @param {string} id - ID de la serie
 * @returns {Object|undefined}
 */
export function getSeriesById(id) {
    return SERIES_DATABASE.find(s => s.id === id);
}

/**
 * Obtiene todas las series de un sector
 * @param {string} sectorId - ID del sector
 * @returns {Array}
 */
export function getSeriesBySector(sectorId) {
    return SERIES_DATABASE.filter(s => s.sectors.includes(sectorId));
}

/**
 * Obtiene todas las series de un tipo de instalación
 * @param {string} installationType - Tipo de instalación
 * @returns {Array}
 */
export function getSeriesByInstallation(installationType) {
    return SERIES_DATABASE.filter(s => s.installation === installationType);
}

export default SERIES_DATABASE;
