/**
 * =============================================================================
 * BOMBAS IDEAL - BIPS Filter Engine
 * =============================================================================
 * 
 * @description  Motor de filtrado para el selector de bombas BIPS.
 *               Procesa los parámetros del usuario y devuelve las series
 *               compatibles ordenadas por relevancia.
 * 
 * @author       Bombas Ideal Development Team
 * @version      4.1.0
 * @module       bips/filter
 */

import { SERIES_DATABASE, SECTORS } from './data.js';

/**
 * Configuración del filtro
 * @constant {Object}
 */
const FILTER_CONFIG = {
    // Margen de tolerancia para caudal y altura (%)
    toleranceMargin: 0.15,
    
    // Peso de cada criterio en el score
    weights: {
        flowMatch: 30,
        headMatch: 30,
        sectorMatch: 25,
        efficiencyBonus: 10,
        materialBonus: 5,
    },
    
    // Score mínimo para considerar una coincidencia
    minScore: 40,
};

/**
 * Parámetros de filtro por defecto
 * @constant {Object}
 */
export const DEFAULT_PARAMS = {
    flow: null,           // Caudal requerido (m³/h)
    head: null,           // Altura requerida (m)
    sector: null,         // Sector/aplicación
    installation: null,   // Tipo de instalación
    material: null,       // Material preferido
    phase: null,          // Fase eléctrica
    maxPower: null,       // Potencia máxima (kW)
    solidsRequired: false, // Requiere paso de sólidos
};

/**
 * Resultado de filtrado
 * @typedef {Object} FilterResult
 * @property {Array} matches - Series que coinciden
 * @property {number} total - Total de coincidencias
 * @property {Object} params - Parámetros usados
 * @property {number} timestamp - Timestamp del filtrado
 */

/**
 * Verifica si un valor está dentro del rango con tolerancia
 * @param {number} value - Valor a verificar
 * @param {Object} range - Objeto con min y max
 * @param {number} [tolerance=0.15] - Margen de tolerancia (0-1)
 * @returns {boolean}
 */
function isInRange(value, range, tolerance = FILTER_CONFIG.toleranceMargin) {
    if (value === null || value === undefined) return true;
    
    const minWithTolerance = range.min * (1 - tolerance);
    const maxWithTolerance = range.max * (1 + tolerance);
    
    return value >= minWithTolerance && value <= maxWithTolerance;
}

/**
 * Calcula el porcentaje de coincidencia de un valor en un rango
 * @param {number} value - Valor del usuario
 * @param {Object} range - Rango de la serie
 * @returns {number} - Porcentaje (0-100)
 */
function calculateRangeMatch(value, range) {
    if (value === null || value === undefined) return 100;
    
    const rangeSpan = range.max - range.min;
    const optimalPoint = range.min + rangeSpan * 0.5; // Punto óptimo al 50%
    
    // Si está dentro del rango, calcular qué tan centrado está
    if (value >= range.min && value <= range.max) {
        const distanceFromOptimal = Math.abs(value - optimalPoint);
        const maxDistance = rangeSpan / 2;
        return 100 - (distanceFromOptimal / maxDistance) * 30; // Max penalización 30%
    }
    
    // Si está fuera pero dentro de tolerancia
    const tolerance = FILTER_CONFIG.toleranceMargin;
    if (value < range.min) {
        const minWithTol = range.min * (1 - tolerance);
        if (value >= minWithTol) {
            return 70 - ((range.min - value) / (range.min - minWithTol)) * 20;
        }
    } else {
        const maxWithTol = range.max * (1 + tolerance);
        if (value <= maxWithTol) {
            return 70 - ((value - range.max) / (maxWithTol - range.max)) * 20;
        }
    }
    
    return 0; // Fuera de rango
}

/**
 * Calcula el score de coincidencia de una serie
 * @param {Object} series - Datos de la serie
 * @param {Object} params - Parámetros del usuario
 * @returns {Object} - { score, breakdown }
 */
function calculateScore(series, params) {
    const breakdown = {};
    let totalScore = 0;
    const weights = FILTER_CONFIG.weights;
    
    // 1. Coincidencia de caudal
    if (params.flow !== null) {
        const flowMatch = calculateRangeMatch(params.flow, series.flow);
        breakdown.flow = flowMatch;
        totalScore += (flowMatch / 100) * weights.flowMatch;
    } else {
        breakdown.flow = 100;
        totalScore += weights.flowMatch;
    }
    
    // 2. Coincidencia de altura
    if (params.head !== null) {
        const headMatch = calculateRangeMatch(params.head, series.head);
        breakdown.head = headMatch;
        totalScore += (headMatch / 100) * weights.headMatch;
    } else {
        breakdown.head = 100;
        totalScore += weights.headMatch;
    }
    
    // 3. Coincidencia de sector
    if (params.sector !== null) {
        const sectorMatch = series.sectors.includes(params.sector) ? 100 : 0;
        breakdown.sector = sectorMatch;
        totalScore += (sectorMatch / 100) * weights.sectorMatch;
    } else {
        breakdown.sector = 100;
        totalScore += weights.sectorMatch;
    }
    
    // 4. Bonus por eficiencia
    const efficiencyBonus = (series.efficiency / 100) * weights.efficiencyBonus;
    breakdown.efficiency = series.efficiency;
    totalScore += efficiencyBonus;
    
    // 5. Bonus por material (si coincide con preferencia)
    if (params.material !== null && series.material === params.material) {
        breakdown.materialMatch = true;
        totalScore += weights.materialBonus;
    }
    
    return {
        score: Math.round(totalScore),
        breakdown,
    };
}

/**
 * Filtra las series según los parámetros dados
 * @param {Object} params - Parámetros de filtrado
 * @returns {FilterResult}
 */
export function filterSeries(params = {}) {
    const mergedParams = { ...DEFAULT_PARAMS, ...params };
    const results = [];
    
    for (const series of SERIES_DATABASE) {
        // Filtros excluyentes (hard filters)
        
        // Verificar rango de caudal
        if (mergedParams.flow !== null) {
            if (!isInRange(mergedParams.flow, series.flow)) {
                continue;
            }
        }
        
        // Verificar rango de altura
        if (mergedParams.head !== null) {
            if (!isInRange(mergedParams.head, series.head)) {
                continue;
            }
        }
        
        // Verificar tipo de instalación
        if (mergedParams.installation !== null) {
            if (series.installation !== mergedParams.installation) {
                continue;
            }
        }
        
        // Verificar fase eléctrica
        if (mergedParams.phase !== null) {
            if (series.phase !== 'both' && series.phase !== mergedParams.phase) {
                continue;
            }
        }
        
        // Verificar potencia máxima
        if (mergedParams.maxPower !== null) {
            if (series.power.min > mergedParams.maxPower) {
                continue;
            }
        }
        
        // Verificar paso de sólidos
        if (mergedParams.solidsRequired && series.solids === 0) {
            continue;
        }
        
        // Calcular score de coincidencia
        const { score, breakdown } = calculateScore(series, mergedParams);
        
        // Solo incluir si supera el score mínimo
        if (score >= FILTER_CONFIG.minScore) {
            results.push({
                ...series,
                matchScore: score,
                matchBreakdown: breakdown,
            });
        }
    }
    
    // Ordenar por score descendente
    results.sort((a, b) => b.matchScore - a.matchScore);
    
    return {
        matches: results,
        total: results.length,
        params: mergedParams,
        timestamp: Date.now(),
    };
}

/**
 * Obtiene sugerencias de series basadas en un sector
 * @param {string} sectorId - ID del sector
 * @param {number} [limit=6] - Número máximo de sugerencias
 * @returns {Array}
 */
export function getSuggestionsBySector(sectorId, limit = 6) {
    const filtered = SERIES_DATABASE.filter(s => s.sectors.includes(sectorId));
    
    // Ordenar por eficiencia
    filtered.sort((a, b) => b.efficiency - a.efficiency);
    
    return filtered.slice(0, limit);
}

/**
 * Obtiene las series más populares/recomendadas
 * @param {number} [limit=6] - Número máximo
 * @returns {Array}
 */
export function getPopularSeries(limit = 6) {
    // Ordenar por eficiencia y versatilidad (número de sectores)
    const ranked = [...SERIES_DATABASE].sort((a, b) => {
        const scoreA = a.efficiency + a.sectors.length * 5;
        const scoreB = b.efficiency + b.sectors.length * 5;
        return scoreB - scoreA;
    });
    
    return ranked.slice(0, limit);
}

/**
 * Valida los parámetros de entrada
 * @param {Object} params - Parámetros a validar
 * @returns {Object} - { valid, errors }
 */
export function validateParams(params) {
    const errors = [];
    
    if (params.flow !== null && params.flow !== undefined) {
        if (typeof params.flow !== 'number' || params.flow <= 0) {
            errors.push('El caudal debe ser un número positivo');
        }
        if (params.flow > 10000) {
            errors.push('El caudal máximo es 10.000 m³/h');
        }
    }
    
    if (params.head !== null && params.head !== undefined) {
        if (typeof params.head !== 'number' || params.head <= 0) {
            errors.push('La altura debe ser un número positivo');
        }
        if (params.head > 300) {
            errors.push('La altura máxima es 300 m');
        }
    }
    
    if (params.sector !== null && params.sector !== undefined) {
        if (!SECTORS[params.sector]) {
            errors.push('Sector no válido');
        }
    }
    
    return {
        valid: errors.length === 0,
        errors,
    };
}

export default {
    filterSeries,
    getSuggestionsBySector,
    getPopularSeries,
    validateParams,
    DEFAULT_PARAMS,
};
